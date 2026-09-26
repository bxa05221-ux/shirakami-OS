"""R0100 end-to-end Evidence-driven Runtime pipeline.

This composes existing Runtime execution with the Evolution Loop. Analysis is
deterministic and provider-neutral; Human approval remains an explicit boundary.
"""

from dataclasses import dataclass
from typing import Any, Callable, Mapping

try:
    from .evidence import EvidenceRecord, capture_evidence
    from .evolution_bridge import (
        ContextSnapshot,
        MismatchEvidence,
        ProtocolCandidate,
        VerificationResult,
        candidate_to_evidence,
        mismatch_to_evidence,
        transition_to_evidence,
    )
    from .evolution_loop import EvolutionLoop, LoopState
    from .evidence_store import EvidenceStore
    from .prototype import ExecutionResult, Runtime, Transition
except ImportError:  # legacy top-level runtime test imports
    from evidence import EvidenceRecord, capture_evidence
    from evolution_bridge import (
        ContextSnapshot,
        MismatchEvidence,
        ProtocolCandidate,
        VerificationResult,
        candidate_to_evidence,
        mismatch_to_evidence,
        transition_to_evidence,
    )
    from evolution_loop import EvolutionLoop, LoopState
    from evidence_store import EvidenceStore
    from prototype import ExecutionResult, Runtime, Transition


@dataclass(frozen=True)
class AnalysisInput:
    observation: Mapping[str, Any]
    evidence: tuple[EvidenceRecord, ...]
    protocol_id: str
    context: ContextSnapshot


@dataclass(frozen=True)
class AnalysisResult:
    protocol_id: str
    candidate: ProtocolCandidate | None
    rationale: str
    source_evidence: tuple[EvidenceRecord, ...] = ()


@dataclass(frozen=True)
class EvolutionRun:
    analysis: AnalysisResult
    execution: ExecutionResult | None
    verification: VerificationResult | None
    evidence: tuple[EvidenceRecord, ...]


class EvidenceDrivenRuntime:
    """Composition boundary for one human-gated R0100 cycle."""

    def __init__(
        self,
        store: EvidenceStore | None = None,
        runtime: Runtime | None = None,
    ) -> None:
        self.store = store or EvidenceStore()
        self.runtime = runtime or Runtime()
        self.loop = EvolutionLoop()
        self._evidence_cursor = 0
        self._observation: dict[str, Any] = {}
        self._context = ContextSnapshot()
        self._candidate: ProtocolCandidate | None = None

    def observe(
        self,
        observation: Mapping[str, Any],
        context: ContextSnapshot,
    ) -> None:
        self.loop.dispatch("observe", observation)
        self.store = self.store.extend(self._loop_evidence())
        self.loop.dispatch("evidence", observation)
        self.store = self.store.extend(self._loop_evidence())

        self._observation = dict(observation)
        self._context = context
        self.store = self.store.append(
            EvidenceRecord(
                protocol_id=context.protocol_id or "R0100",
                status="observed",
                transition_kind="R0100:context_snapshot",
                transition_data=context.as_mapping(),
                signals=("CONTEXT_SNAPSHOT",),
            )
        )

    def analyze(
        self,
        protocol_id: str,
        *,
        protocol_exists: bool = True,
        diff_ref: str = "",
    ) -> AnalysisResult:
        relevant = self.store.by_protocol(protocol_id)

        result = self.loop.dispatch(
            "analyze",
            {"protocol_id": protocol_id},
        )
        if not result.accepted:
            raise RuntimeError(f"analysis transition failed: {result.reason}")

        if protocol_exists:
            rationale = "Existing protocol selected from current context."
            result = self.loop.dispatch(
                "existing_protocol",
                {"protocol_id": protocol_id},
            )
            if not result.accepted:
                raise RuntimeError(f"protocol selection failed: {result.reason}")
            self.store = self.store.extend(self._loop_evidence())
            return AnalysisResult(protocol_id, None, rationale, relevant)

        candidate = ProtocolCandidate(
            protocol_id=protocol_id,
            diff_ref=diff_ref,
            rationale="No existing protocol selected; candidate requires Human Review.",
            source_evidence=tuple(
                f"{record.protocol_id}:{record.transition_kind}"
                for record in relevant
            ),
        )
        self._candidate = candidate

        result = self.loop.dispatch(
            "new_protocol",
            {
                "protocol_id": protocol_id,
                "diff_ref": diff_ref,
                "rationale": candidate.rationale,
            },
        )
        if not result.accepted:
            raise RuntimeError(f"candidate transition failed: {result.reason}")

        self.store = self.store.extend(self._loop_evidence())
        self.store = self.store.append(
            candidate_to_evidence(
                self.loop.evidence[-1],
                protocol_id=protocol_id,
            )
        )

        result = self.loop.dispatch(
            "review",
            {"protocol_id": protocol_id, "diff_ref": diff_ref},
        )
        if not result.accepted:
            raise RuntimeError(f"human review transition failed: {result.reason}")
        self.store = self.store.extend(self._loop_evidence())

        return AnalysisResult(
            protocol_id,
            candidate,
            candidate.rationale,
            relevant,
        )

    def approve(
        self,
        *,
        approved: bool = True,
        reviewer: str = "human",
    ) -> bool:
        """Resolve HUMAN_REVIEW with an explicit human decision."""
        if self.loop.state is not LoopState.HUMAN_REVIEW:
            return False

        event = "approve" if approved else "reject"
        result = self.loop.dispatch(
            event,
            {
                "protocol_id": self._candidate.protocol_id if self._candidate else "",
                "reviewer": reviewer,
                "decision": "approved" if approved else "rejected",
            },
            human_approved=True,
        )
        self.store = self.store.extend(self._loop_evidence())
        return result.accepted

    def execute(
        self,
        protocol: Callable[[Any], Transition],
        protocol_id: str,
        input_data: Mapping[str, Any] | None = None,
        model_output: Any | None = None,
    ) -> ExecutionResult:
        if self.loop.state is LoopState.READY:
            gate = self.loop.dispatch(
                "execute",
                {"protocol_id": protocol_id},
            )
            if not gate.accepted:
                raise RuntimeError(f"execution gate failed: {gate.reason}")

        if self.loop.state is not LoopState.EXECUTE:
            raise RuntimeError(
                f"runtime not ready for execution: {self.loop.state.value}"
            )

        result = self.runtime.execute(protocol_id, protocol, input_data)
        self.store = self.store.append(capture_evidence(result, model_output=model_output))

        gate = self.loop.dispatch("verify", {"status": result.status})
        if not gate.accepted:
            raise RuntimeError(
                f"verification transition failed: {gate.reason}"
            )
        self.store = self.store.extend(self._loop_evidence())
        return result

    def verify(
        self,
        execution: ExecutionResult,
        *,
        expected_transition_kind: str | None = None,
        diff_ref: str = "",
    ) -> VerificationResult:
        observed = execution.transition.kind
        matched = (
            expected_transition_kind is None
            or observed == expected_transition_kind
        )
        verification = VerificationResult(
            status="pass" if matched else "mismatch",
            uncertainty="low" if matched else "medium",
            observed={
                "transition_kind": observed,
                "expected_transition_kind": expected_transition_kind,
                "execution_status": execution.status,
            },
        )

        result = self.loop.dispatch(
            "pass" if matched else "mismatch",
            verification.observed,
        )
        if not result.accepted:
            raise RuntimeError(
                f"verification result transition failed: {result.reason}"
            )
        self.store = self.store.extend(self._loop_evidence())

        if not matched:
            mismatch = MismatchEvidence(
                protocol_id=execution.protocol_id,
                diff_ref=diff_ref,
                expected=expected_transition_kind,
                observed=observed,
                uncertainty=verification.uncertainty,
                source_evidence=(f"R0100:{execution.transition.kind}",),
                context=self._context.as_mapping(),
            )
            self.store = self.store.append(mismatch_to_evidence(mismatch))

        return verification

    def _loop_evidence(self) -> tuple[EvidenceRecord, ...]:
        records: list[EvidenceRecord] = []
        new_records = self.loop.records[self._evidence_cursor:]
        self._evidence_cursor = len(self.loop.records)
        for record in new_records:
            evidence = transition_to_evidence(record)
            if evidence is not None:
                records.append(evidence)
        return tuple(records)


def example_cycle(
    protocol: Callable[[Any], Transition],
    protocol_id: str,
    observation: Mapping[str, Any],
    context: ContextSnapshot,
) -> EvolutionRun:
    runtime = EvidenceDrivenRuntime()
    runtime.observe(observation, context)
    analysis = runtime.analyze(protocol_id)
    execution = runtime.execute(protocol, protocol_id, observation)
    verification = runtime.verify(execution)
    return EvolutionRun(
        analysis,
        execution,
        verification,
        runtime.store.all(),
    )

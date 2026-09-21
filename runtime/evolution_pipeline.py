"""R0100 end-to-end Evidence-driven Runtime pipeline.

This composes existing Runtime execution with the Evolution Loop.  Analysis is
kept deterministic and provider-neutral; Human approval remains an explicit
boundary.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from .evidence import EvidenceRecord, capture_evidence
from .evolution_bridge import ContextSnapshot, ProtocolCandidate, VerificationResult, transition_to_evidence
from .evolution_loop import EvolutionLoop, LoopState
from .evidence_store import EvidenceStore
from .prototype import ExecutionResult, Runtime, Transition


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
    """Small composition boundary for one human-gated R0100 cycle."""

    def __init__(self, store: EvidenceStore | None = None, runtime: Runtime | None = None) -> None:
        self.store = store or EvidenceStore()
        self.runtime = runtime or Runtime()
        self.loop = EvolutionLoop()

    def observe(self, observation: Mapping[str, Any], context: ContextSnapshot) -> None:
        self.loop.dispatch("observe", observation)
        self.store = self.store.extend(self._loop_evidence())
        self.loop.dispatch("evidence", observation)
        self.store = self.store.extend(self._loop_evidence())
        self._observation = dict(observation)
        self._context = context

    def analyze(self, protocol_id: str) -> AnalysisResult:
        relevant = self.store.by_protocol(protocol_id)
        self.loop.dispatch("analyze", {"protocol_id": protocol_id})
        candidate = ProtocolCandidate(
            protocol_id=protocol_id,
            diff_ref="",
            rationale="Existing protocol selected from current context.",
            source_evidence=tuple(
                f"{record.protocol_id}:{record.transition_kind}" for record in relevant
            ),
        )
        self.loop.dispatch("existing_protocol", {"protocol_id": protocol_id})
        self.store = self.store.extend(self._loop_evidence())
        return AnalysisResult(
            protocol_id=protocol_id,
            candidate=None,
            rationale=candidate.rationale,
            source_evidence=relevant,
        )

    def approve(self) -> None:
        result = self.loop.dispatch("execute", human_approved=True)
        if not result.accepted:
            raise RuntimeError(f"execution gate failed: {result.reason}")

    def execute(
        self,
        protocol: Callable[[Any], Transition],
        protocol_id: str,
        input_data: Mapping[str, Any] | None = None,
    ) -> ExecutionResult:
        if self.loop.state is not LoopState.EXECUTE:
            raise RuntimeError(f"runtime not ready for execution: {self.loop.state.value}")
        result = self.runtime.execute(protocol_id, protocol, input_data)
        evidence = capture_evidence(result)
        self.store = self.store.append(evidence)
        self.loop.dispatch("verify", {"status": result.status})
        self.store = self.store.extend(self._loop_evidence())
        return result

    def verify(
        self,
        execution: ExecutionResult,
        *,
        expected_transition_kind: str | None = None,
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
        if matched:
            self.loop.dispatch("pass", verification.observed)
        else:
            self.loop.dispatch("mismatch", verification.observed)
        self.store = self.store.extend(self._loop_evidence())
        return verification

    def _loop_evidence(self) -> tuple[EvidenceRecord, ...]:
        records = []
        for record in self.loop.records[len(records):]:
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
    runtime.approve()
    execution = runtime.execute(protocol, protocol_id, observation)
    verification = runtime.verify(execution)
    return EvolutionRun(analysis, execution, verification, runtime.store.all())

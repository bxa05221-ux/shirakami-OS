"""Provider-neutral UI for AI API boundary α0.1."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4
from typing import Any, Callable, Mapping

try:
    from .evolution_bridge import ContextSnapshot, VerificationResult
    from .evolution_pipeline import AnalysisResult, EvidenceDrivenRuntime
    from .prototype import ExecutionResult, Transition
    from .trace import ExecutionTrace, ExecutionTraceStore
except ImportError:
    from evolution_bridge import ContextSnapshot, VerificationResult
    from evolution_pipeline import AnalysisResult, EvidenceDrivenRuntime
    from prototype import ExecutionResult, Transition
    from trace import ExecutionTrace, ExecutionTraceStore


@dataclass(frozen=True)
class ExecutionHandle:
    """Immutable reference to one externally addressable execution."""
    execution_id: str
    protocol_id: str
    status: str
    result: dict[str, Any]
    handoff_id: str | None = None
    trace_id: str | None = None
    evidence_ids: tuple[str, ...] = ()
    project: str | None = None
    objective: str | None = None
    protocol_ids: tuple[str, ...] = ()
    verification_scope: tuple[Any, ...] = ()


class ExecutionHandleStore:
    """Append-only in-memory execution-handle boundary for alpha 0.2."""

    def __init__(self) -> None:
        self._records: dict[str, ExecutionHandle] = {}

    def create(
        self, protocol_id: str, result: dict[str, Any], *,
        handoff_id: str | None = None, trace_id: str | None = None,
        evidence_ids: tuple[str, ...] = (), project: str | None = None,
        objective: str | None = None, protocol_ids: tuple[str, ...] = (),
        verification_scope: tuple[Any, ...] = (),
    ) -> ExecutionHandle:
        handle = ExecutionHandle(
            str(uuid4()), protocol_id, result.get("status", "unknown"), dict(result),
            handoff_id, trace_id, tuple(evidence_ids), project, objective,
            tuple(protocol_ids), tuple(verification_scope),
        )
        self._records[handle.execution_id] = handle
        return handle

    def get(self, execution_id: str) -> ExecutionHandle | None:
        return self._records.get(execution_id)


class ShirakamiAPI:
    """Bidirectional semantic boundary between UI/external systems and Runtime."""

    def __init__(
        self,
        runtime: EvidenceDrivenRuntime | None = None,
        executions: ExecutionHandleStore | None = None,
        traces: ExecutionTraceStore | None = None,
    ) -> None:
        self.runtime = runtime or EvidenceDrivenRuntime()
        self.executions = executions or ExecutionHandleStore()
        self.traces = traces or ExecutionTraceStore()

    def observe(self, observation: Mapping[str, Any], context: ContextSnapshot) -> dict[str, Any]:
        self.runtime.observe(observation, context)
        return {"state": self.runtime.loop.state.value, "evidence": self._evidence()}

    def analyze(self, protocol_id: str, *, protocol_exists: bool = True, diff_ref: str = "") -> AnalysisResult:
        return self.runtime.analyze(protocol_id, protocol_exists=protocol_exists, diff_ref=diff_ref)

    def approve(
        self, *, approved: bool = True, reviewer: str = "human", human_authorized: bool = False
    ) -> dict[str, Any]:
        if not human_authorized:
            return {
                "accepted": False,
                "state": self.runtime.loop.state.value,
                "reason": "explicit human authorization required",
            }
        accepted = self.runtime.approve(approved=approved, reviewer=reviewer)
        return {"accepted": accepted, "state": self.runtime.loop.state.value}

    def execute(
        self, protocol: Callable[[Any], Transition], protocol_id: str,
        input_data: Mapping[str, Any] | None = None, *,
        handoff_id: str | None = None, trace_id: str | None = None,
        evidence_ids: tuple[str, ...] = (), project: str | None = None,
        objective: str | None = None, protocol_ids: tuple[str, ...] = (),
        verification_scope: tuple[Any, ...] = (),
    ) -> dict[str, Any]:
        result = self.runtime.execute(protocol, protocol_id, input_data)
        evidence = self._evidence_for_protocol(protocol_id)[-1:]
        payload = {
            "status": result.status,
            "protocol_id": result.protocol_id,
            "transition": {"kind": result.transition.kind, "data": dict(result.transition.data)},
            "signals": list(result.signals),
            "steps": result.steps,
            "evidence": evidence,
            "handoff_id": handoff_id,
            "trace_id": trace_id,
            "evidence_ids": list(evidence_ids),
            "project": project,
            "objective": objective,
            "protocol_ids": list(protocol_ids),
            "verification_scope": list(verification_scope),
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        }
        provisional_trace_id = trace_id or f"TRACE-{uuid4()}"
        handle = self.executions.create(
            protocol_id, payload, handoff_id=handoff_id, trace_id=provisional_trace_id,
            evidence_ids=evidence_ids, project=project, objective=objective,
            protocol_ids=protocol_ids, verification_scope=verification_scope,
        )
        resolved_trace_id = provisional_trace_id
        if evidence and not evidence_ids:
            linked_evidence_ids = tuple(item["evidence_id"] for item in evidence)
        else:
            linked_evidence_ids = tuple(evidence_ids)
        self.traces.create(ExecutionTrace(
            trace_id=resolved_trace_id,
            execution_id=handle.execution_id,
            handoff_id=handoff_id,
            evidence_ids=linked_evidence_ids,
            project=project,
            objective=objective,
            protocol_ids=tuple(protocol_ids),
            verification_scope=tuple(verification_scope),
        ))
        payload["trace_id"] = resolved_trace_id
        return {**payload, "execution_id": handle.execution_id, "trace_id": resolved_trace_id}

    def get_execution(self, execution_id: str) -> dict[str, Any] | None:
        handle = self.executions.get(execution_id)
        if handle is None:
            return None
        return {
            "execution_id": handle.execution_id, "protocol_id": handle.protocol_id,
            "status": handle.status, "result": dict(handle.result),
            "handoff_id": handle.handoff_id, "trace_id": handle.trace_id,
            "evidence_ids": list(handle.evidence_ids), "project": handle.project,
            "objective": handle.objective, "protocol_ids": list(handle.protocol_ids),
            "verification_scope": list(handle.verification_scope),
        }

    def get_trace(self, trace_id: str) -> dict[str, Any] | None:
        trace = self.traces.get(trace_id)
        if trace is None:
            return None
        return {
            "trace_id": trace.trace_id,
            "execution_id": trace.execution_id,
            "handoff_id": trace.handoff_id,
            "evidence_ids": list(trace.evidence_ids),
            "project": trace.project,
            "objective": trace.objective,
            "protocol_ids": list(trace.protocol_ids),
            "verification_scope": list(trace.verification_scope),
            "verification_status": trace.verification_status,
            "verification_uncertainty": trace.verification_uncertainty,
            "verification_observed": dict(trace.verification_observed),
            "commit": trace.commit,
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        }

    def verify_execution(
        self, execution_id: str, *, expected_transition_kind: str | None = None,
        diff_ref: str = "",
    ) -> VerificationResult | None:
        handle = self.executions.get(execution_id)
        if handle is None:
            return None
        payload = handle.result
        transition = payload["transition"]
        execution = ExecutionResult(
            status=str(payload["status"]), protocol_id=str(payload["protocol_id"]),
            transition=Transition(kind=str(transition["kind"]), data=dict(transition.get("data", {}))),
            signals=tuple(payload.get("signals", ())), steps=int(payload.get("steps", 0)),
        )
        verification = self.verify(execution, expected_transition_kind=expected_transition_kind, diff_ref=diff_ref)
        if handle.trace_id is not None:
            self.traces.attach_verification(
                handle.trace_id,
                status=verification.status,
                uncertainty=verification.uncertainty,
                observed=verification.observed,
            )
        return verification

    def verify(
        self, execution: ExecutionResult, *, expected_transition_kind: str | None = None,
        diff_ref: str = "",
    ) -> VerificationResult:
        return self.runtime.verify(
            execution, expected_transition_kind=expected_transition_kind, diff_ref=diff_ref
        )

    def query_evidence(
        self, *, protocol_id: str | None = None, signal: str | None = None,
        transition_kind: str | None = None,
    ) -> tuple[Any, ...]:
        if protocol_id is not None:
            records = self.runtime.store.by_protocol(protocol_id)
        elif signal is not None:
            records = self.runtime.store.by_signal(signal)
        elif transition_kind is not None:
            records = self.runtime.store.by_transition(transition_kind)
        else:
            records = self.runtime.store.all()
        return tuple(self._serialize_evidence(record) for record in records)

    def _evidence(self) -> list[dict[str, Any]]:
        return [self._serialize_evidence(record) for record in self.runtime.store.all()]

    def _evidence_for_protocol(self, protocol_id: str) -> list[dict[str, Any]]:
        return [self._serialize_evidence(record) for record in self.runtime.store.by_protocol(protocol_id)]

    @staticmethod
    def _serialize_evidence(record: Any) -> dict[str, Any]:
        return {
            "evidence_id": record.evidence_id,
            "protocol_id": record.protocol_id,
            "status": record.status,
            "transition_kind": record.transition_kind,
            "transition_data": dict(record.transition_data),
            "signals": list(record.signals),
            "confidence": record.confidence,
        }

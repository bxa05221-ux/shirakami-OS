"""Provider-neutral UI for AI API boundary α0.1.

This module exposes the semantic API around the R0100 Evidence-driven Runtime.
Transport concerns (HTTP, CLI, desktop UI, robot controller, etc.) remain outside
this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4
from typing import Any, Callable, Mapping

try:
    from .evolution_bridge import ContextSnapshot, VerificationResult
    from .evolution_pipeline import AnalysisResult, EvidenceDrivenRuntime
    from .prototype import ExecutionResult, Transition
    from .semantic_handoff import SemanticHandoff
except ImportError:
    from evolution_bridge import ContextSnapshot, VerificationResult
    from evolution_pipeline import AnalysisResult, EvidenceDrivenRuntime
    from prototype import ExecutionResult, Transition
    from semantic_handoff import SemanticHandoff


@dataclass(frozen=True)
class ExecutionHandle:
    """Immutable reference to one externally addressable execution."""
    execution_id: str
    protocol_id: str
    status: str
    result: dict[str, Any]


class ExecutionHandleStore:
    """Append-only in-memory execution-handle boundary for alpha 0.2."""
    def __init__(self) -> None:
        self._records: dict[str, ExecutionHandle] = {}

    def create(self, protocol_id: str, result: dict[str, Any]) -> ExecutionHandle:
        handle = ExecutionHandle(str(uuid4()), protocol_id, result.get("status", "unknown"), dict(result))
        self._records[handle.execution_id] = handle
        return handle

    def get(self, execution_id: str) -> ExecutionHandle | None:
        return self._records.get(execution_id)


class ShirakamiAPI:
    """Bidirectional semantic boundary between UI/external systems and Runtime."""

    def __init__(self, runtime: EvidenceDrivenRuntime | None = None, executions: ExecutionHandleStore | None = None) -> None:
        self.runtime = runtime or EvidenceDrivenRuntime()
        self.executions = executions or ExecutionHandleStore()

    def observe(
        self,
        observation: Mapping[str, Any],
        context: ContextSnapshot,
    ) -> dict[str, Any]:
        evidence_before = len(self.runtime.store.all())
        self.runtime.observe(observation, context)
        evidence_records = self.runtime.store.all()
        new_evidence = evidence_records[evidence_before:]

        observation_id = str(uuid4())
        handoff = SemanticHandoff(
            observation_id=observation_id,
            landscape=context.landscape,
            protocol_id=context.protocol_id,
            runtime_state=self.runtime.loop.state.value,
            evidence_ids=tuple(record.evidence_id for record in new_evidence),
            metadata=context.metadata,
        )
        return {
            "state": self.runtime.loop.state.value,
            "evidence": self._evidence(),
            "semantic_handoff": dict(handoff.as_mapping()),
        }

    def analyze(self, protocol_id: str, *, protocol_exists: bool = True, diff_ref: str = "") -> AnalysisResult:
        return self.runtime.analyze(protocol_id, protocol_exists=protocol_exists, diff_ref=diff_ref)

    def approve(self, *, approved: bool = True, reviewer: str = "human", human_authorized: bool = False) -> dict[str, Any]:
        if not human_authorized:
            return {"accepted": False, "state": self.runtime.loop.state.value, "reason": "explicit human authorization required"}
        accepted = self.runtime.approve(approved=approved, reviewer=reviewer)
        return {"accepted": accepted, "state": self.runtime.loop.state.value}

    def execute(self, protocol: Callable[[Any], Transition], protocol_id: str, input_data: Mapping[str, Any] | None = None) -> dict[str, Any]:
        result = self.runtime.execute(protocol, protocol_id, input_data)
        payload = {
            "status": result.status,
            "protocol_id": result.protocol_id,
            "transition": {"kind": result.transition.kind, "data": dict(result.transition.data)},
            "signals": list(result.signals),
            "steps": result.steps,
            "evidence": self._evidence_for_protocol(protocol_id)[-1:],
        }
        handle = self.executions.create(protocol_id, payload)
        return {**payload, "execution_id": handle.execution_id}

    def get_execution(self, execution_id: str) -> dict[str, Any] | None:
        handle = self.executions.get(execution_id)
        if handle is None:
            return None
        return {"execution_id": handle.execution_id, "protocol_id": handle.protocol_id, "status": handle.status, "result": dict(handle.result)}

    def verify_execution(self, execution_id: str, *, expected_transition_kind: str | None = None, diff_ref: str = "") -> VerificationResult | None:
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
        return self.verify(execution, expected_transition_kind=expected_transition_kind, diff_ref=diff_ref)

    def verify(self, execution: ExecutionResult, *, expected_transition_kind: str | None = None, diff_ref: str = "") -> VerificationResult:
        return self.runtime.verify(execution, expected_transition_kind=expected_transition_kind, diff_ref=diff_ref)

    def query_evidence(self, *, protocol_id: str | None = None, signal: str | None = None, transition_kind: str | None = None) -> tuple[Any, ...]:
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

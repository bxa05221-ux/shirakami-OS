"""Provider-neutral UI for AI API boundary α0.1.

This module exposes the semantic API around the R0100 Evidence-driven Runtime.
Transport concerns (HTTP, CLI, desktop UI, robot controller, etc.) remain outside
this module.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Callable, Mapping

try:
    from .evolution_bridge import ContextSnapshot, VerificationResult
    from .evolution_pipeline import AnalysisResult, EvidenceDrivenRuntime
    from .prototype import ExecutionResult, Transition
except ImportError:
    from evolution_bridge import ContextSnapshot, VerificationResult
    from evolution_pipeline import AnalysisResult, EvidenceDrivenRuntime
    from prototype import ExecutionResult, Transition


class ShirakamiAPI:
    """Bidirectional semantic boundary between UI/external systems and Runtime."""

    def __init__(self, runtime: EvidenceDrivenRuntime | None = None) -> None:
        self.runtime = runtime or EvidenceDrivenRuntime()

    def observe(
        self,
        observation: Mapping[str, Any],
        context: ContextSnapshot,
    ) -> dict[str, Any]:
        self.runtime.observe(observation, context)
        return {
            "state": self.runtime.loop.state.value,
            "evidence": self._evidence(),
        }

    def analyze(
        self,
        protocol_id: str,
        *,
        protocol_exists: bool = True,
        diff_ref: str = "",
    ) -> AnalysisResult:
        return self.runtime.analyze(
            protocol_id,
            protocol_exists=protocol_exists,
            diff_ref=diff_ref,
        )

    def approve(
        self,
        *,
        approved: bool = True,
        reviewer: str = "human",
        human_authorized: bool = False,
    ) -> dict[str, Any]:
        """Apply an explicit human decision; authorization is never inferred."""
        if not human_authorized:
            return {
                "accepted": False,
                "state": self.runtime.loop.state.value,
                "reason": "explicit human authorization required",
            }

        accepted = self.runtime.approve(
            approved=approved,
            reviewer=reviewer,
        )
        return {
            "accepted": accepted,
            "state": self.runtime.loop.state.value,
        }

    def execute(
        self,
        protocol: Callable[[Any], Transition],
        protocol_id: str,
        input_data: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        result = self.runtime.execute(protocol, protocol_id, input_data)
        return {
            "status": result.status,
            "transition": {
                "kind": result.transition.kind,
                "data": dict(result.transition.data),
            },
            "signals": list(result.signals),
            "evidence": self._evidence_for_protocol(protocol_id)[-1:]
        }

    def verify(
        self,
        execution: ExecutionResult,
        *,
        expected_transition_kind: str | None = None,
        diff_ref: str = "",
    ) -> VerificationResult:
        return self.runtime.verify(
            execution,
            expected_transition_kind=expected_transition_kind,
            diff_ref=diff_ref,
        )

    def query_evidence(
        self,
        *,
        protocol_id: str | None = None,
        signal: str | None = None,
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
        return [
            self._serialize_evidence(record)
            for record in self.runtime.store.by_protocol(protocol_id)
        ]

    @staticmethod
    def _serialize_evidence(record: Any) -> dict[str, Any]:
        return {
            "protocol_id": record.protocol_id,
            "status": record.status,
            "transition_kind": record.transition_kind,
            "transition_data": dict(record.transition_data),
            "signals": list(record.signals),
            "confidence": record.confidence,
        }

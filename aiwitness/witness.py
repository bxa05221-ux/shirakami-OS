"""Provider-neutral AIwitness observation boundary.

AIwitness records observed execution provenance without modifying the source
trace or introducing execution, publication, merge, or human-gate authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.trace import ExecutionTrace


_ALLOWED_STATUS = {"pending", "pass", "fail"}


@dataclass(frozen=True)
class WitnessRecord:
    trace_id: str
    execution_id: str
    handoff_id: str
    evidence_ids: tuple[str, ...]
    verification_status: str
    commit: str | None
    verification_uncertainty: str | None
    verification_observed: Mapping[str, Any]
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False
    human_gate_required: bool = True

    def __post_init__(self) -> None:
        if not self.trace_id or not self.execution_id or not self.handoff_id:
            raise ValueError("witness identity must be non-empty")
        if self.verification_status not in _ALLOWED_STATUS:
            raise ValueError("unsupported verification status")
        if self.execution_authorized or self.publish_authorized or self.merge_authorized:
            raise ValueError("AIwitness cannot grant authority")
        if not self.human_gate_required:
            raise ValueError("human_gate_required must remain true")
        object.__setattr__(
            self,
            "verification_observed",
            dict(self.verification_observed),
        )


class AIwitness:
    """Observe an ExecutionTrace without changing it."""

    @staticmethod
    def observe(trace: ExecutionTrace) -> WitnessRecord:
        if trace.handoff_id is None:
            raise ValueError("AIwitness requires handoff_id")

        return WitnessRecord(
            trace_id=trace.trace_id,
            execution_id=trace.execution_id,
            handoff_id=trace.handoff_id,
            evidence_ids=tuple(trace.evidence_ids),
            verification_status=trace.verification_status,
            commit=trace.commit,
            verification_uncertainty=trace.verification_uncertainty,
            verification_observed=dict(trace.verification_observed),
        )

"""Stable Semantic Handoff envelope for API and external boundaries.

The envelope carries provenance identifiers across boundaries without changing
verification or authority semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .trace import ExecutionTrace


@dataclass(frozen=True)
class SemanticHandoff:
    """Immutable provider-neutral handoff envelope."""

    handoff_id: str
    trace_id: str
    execution_id: str
    activity_id: str | None
    evidence_ids: tuple[str, ...]
    project: str | None
    objective: str | None
    protocol_ids: tuple[str, ...]
    verification_scope: tuple[object, ...]
    verification_status: str
    human_gate_required: bool = True
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False

    def __post_init__(self) -> None:
        if not self.handoff_id:
            raise ValueError("handoff_id must be non-empty")
        if not self.trace_id:
            raise ValueError("trace_id must be non-empty")
        if not self.execution_id:
            raise ValueError("execution_id must be non-empty")
        if any(not item for item in self.evidence_ids):
            raise ValueError("evidence_ids must contain non-empty strings")
        if not self.human_gate_required:
            raise ValueError("human_gate_required must remain true")
        if self.execution_authorized or self.publish_authorized or self.merge_authorized:
            raise ValueError("semantic handoff cannot grant authority")

    @classmethod
    def from_trace(
        cls,
        trace: ExecutionTrace,
        *,
        activity_id: str | None = None,
    ) -> "SemanticHandoff":
        handoff_id = trace.handoff_id
        if not handoff_id:
            raise ValueError("trace must declare handoff_id")
        observed_activity_id = trace.verification_observed.get("activity_id")
        if activity_id is not None and not activity_id:
            raise ValueError("activity_id must be non-empty when supplied")
        if activity_id is not None and observed_activity_id not in (None, activity_id):
            raise ValueError("activity_id does not match trace")
        return cls(
            handoff_id=handoff_id,
            trace_id=trace.trace_id,
            execution_id=trace.execution_id,
            activity_id=activity_id or observed_activity_id,
            evidence_ids=tuple(trace.evidence_ids),
            project=trace.project,
            objective=trace.objective,
            protocol_ids=tuple(trace.protocol_ids),
            verification_scope=tuple(trace.verification_scope),
            verification_status=trace.verification_status,
        )

    def contains_evidence(self, evidence_id: str) -> bool:
        return evidence_id in self.evidence_ids

    def source_ids(self) -> tuple[str, ...]:
        ids = [self.handoff_id, self.trace_id, self.execution_id]
        if self.activity_id:
            ids.append(self.activity_id)
        ids.extend(self.evidence_ids)
        return tuple(dict.fromkeys(ids))

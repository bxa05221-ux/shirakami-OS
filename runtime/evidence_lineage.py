"""Provider-neutral Evidence Lineage boundary.

This module binds externally observed Agent Activity and Runtime execution
traces without changing authority or verification semantics.

The boundary is deliberately descriptive: it does not promote activity,
grant permission, or manufacture Evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .trace import ExecutionTrace


@dataclass(frozen=True)
class EvidenceLineage:
    """Immutable cross-boundary lineage for one Shirakami trace."""

    trace_id: str
    execution_id: str
    handoff_id: str | None
    activity_id: str | None
    evidence_ids: tuple[str, ...]
    sources: tuple[str, ...]
    human_gate_required: bool = True
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False

    def __post_init__(self) -> None:
        if not self.trace_id:
            raise ValueError("trace_id must be non-empty")
        if not self.execution_id:
            raise ValueError("execution_id must be non-empty")
        if any(not item for item in self.evidence_ids):
            raise ValueError("evidence_ids must contain non-empty strings")
        if not self.sources:
            raise ValueError("sources must not be empty")
        if not self.human_gate_required:
            raise ValueError("human_gate_required must remain true")
        if self.execution_authorized or self.publish_authorized or self.merge_authorized:
            raise ValueError("lineage cannot grant authority")


class EvidenceLineageBoundary:
    """Build and validate lineage from an existing ExecutionTrace."""

    def from_trace(
        self,
        trace: ExecutionTrace,
        *,
        activity_id: str | None = None,
        sources: Iterable[str] = (),
    ) -> EvidenceLineage:
        declared_sources = tuple(dict.fromkeys(str(item) for item in sources if str(item)))
        if activity_id is not None and not activity_id:
            raise ValueError("activity_id must be non-empty when supplied")

        observed_activity_id = trace.verification_observed.get("activity_id")
        if activity_id is not None and observed_activity_id not in (None, activity_id):
            raise ValueError("activity_id does not match trace")

        return EvidenceLineage(
            trace_id=trace.trace_id,
            execution_id=trace.execution_id,
            handoff_id=trace.handoff_id,
            activity_id=activity_id or observed_activity_id,
            evidence_ids=tuple(trace.evidence_ids),
            sources=declared_sources or ("execution_trace",),
        )

    def require_evidence(self, lineage: EvidenceLineage, evidence_id: str) -> None:
        if evidence_id not in lineage.evidence_ids:
            raise ValueError("evidence_id is not linked to lineage")

    def require_same_trace(self, *lineages: EvidenceLineage) -> str:
        if not lineages:
            raise ValueError("at least one lineage is required")
        trace_ids = {item.trace_id for item in lineages}
        if len(trace_ids) != 1:
            raise ValueError("lineages must reference the same trace")
        return lineages[0].trace_id

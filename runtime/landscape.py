"""Minimal replaceable Landscape State boundary for Runtime β0.1."""

from dataclasses import dataclass, field
from typing import Any, Mapping

from evidence import EvidenceRecord, is_transition_evidence
from projection import Projection, project_evidence


@dataclass
class LandscapeState:
    """Small in-memory representation of current observable Landscape state."""

    _state: dict[str, Any]
    _projections: list[Projection] = field(default_factory=list)

    @classmethod
    def empty(cls) -> "LandscapeState":
        return cls(_state={})

    def snapshot(self) -> Mapping[str, Any]:
        return dict(self._state)

    def projection_history(self) -> tuple[Projection, ...]:
        """Return immutable history of projections applied to this state."""
        return tuple(self._projections)

    def apply_projection(self, projection: Projection) -> None:
        """Apply a derived Projection, never the source Evidence directly."""
        self._state.update(dict(projection.changes))
        self._projections.append(projection)

    def apply_evidence(self, evidence: EvidenceRecord) -> None:
        """Backward-compatible boundary: Evidence -> Projection -> State."""
        if not is_transition_evidence(evidence):
            return
        self.apply_projection(project_evidence(evidence))

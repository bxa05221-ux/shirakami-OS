"""Minimal navigation state boundary for Shirakami OS.

Navigation observes Landscape-derived state. It does not choose values,
set destinations, or autonomously change course.
"""

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class ReferenceFrame:
    """Human-selected measurement/reference frame."""

    id: str


@dataclass
class NavigationState:
    """Inspectable navigation state, kept separate from Runtime semantics."""

    position: Any = None
    direction: Any = None
    attitude: Any = None
    reference_frame: ReferenceFrame | None = None
    map_id: str = "distorted_celestial_sphere"
    horizon: Any = None
    landscape_revision: int = 0
    evidence_cursor: Any = None
    uncertainty: list[Any] = field(default_factory=list)

    def snapshot(self) -> Mapping[str, Any]:
        return {
            "position": self.position,
            "direction": self.direction,
            "attitude": self.attitude,
            "reference_frame": self.reference_frame.id if self.reference_frame else None,
            "map_id": self.map_id,
            "horizon": self.horizon,
            "landscape_revision": self.landscape_revision,
            "evidence_cursor": self.evidence_cursor,
            "uncertainty": list(self.uncertainty),
        }

    def observe(
        self,
        *,
        position: Any = None,
        direction: Any = None,
        attitude: Any = None,
        horizon: Any = None,
        evidence_cursor: Any = None,
        landscape_changed: bool = False,
        uncertainty: list[Any] | None = None,
    ) -> None:
        """Update observations without making a judgment or changing course."""
        if position is not None:
            self.position = position
        if direction is not None:
            self.direction = direction
        if attitude is not None:
            self.attitude = attitude
        if horizon is not None:
            self.horizon = horizon
        if evidence_cursor is not None:
            self.evidence_cursor = evidence_cursor
        if landscape_changed:
            self.landscape_revision += 1
        if uncertainty is not None:
            self.uncertainty = list(uncertainty)

    def set_reference_frame(self, reference_id: str) -> None:
        """Set a human-selected reference frame; never infer one automatically."""
        if not isinstance(reference_id, str) or not reference_id.strip():
            raise ValueError("reference_id must be a non-empty string")
        self.reference_frame = ReferenceFrame(id=reference_id)


AUTOPILOT_FORBIDDEN_OPERATIONS = frozenset(
    {
        "choose_destination",
        "choose_values",
        "choose_faith",
        "change_course",
        "make_final_decision",
    }
)

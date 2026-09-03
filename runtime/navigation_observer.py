"""Evidence-backed observer for Shirakami navigation state.

The observer only copies explicitly observable navigation fields from immutable
EvidenceRecord data. It never infers a position, direction, reference frame,
destination, value, or course correction.
"""

from typing import Any

from .evidence import EvidenceRecord, is_transition_evidence
from .navigation import NavigationState


_NAVIGATION_FIELDS = frozenset({
    "position",
    "direction",
    "attitude",
    "horizon",
    "uncertainty",
})


class NavigationObserver:
    """Translate observable Evidence into NavigationState without interpretation."""

    def __init__(self, state: NavigationState | None = None) -> None:
        self.state = state or NavigationState()

    def observe(self, evidence: EvidenceRecord) -> NavigationState:
        data: dict[str, Any] = dict(evidence.transition_data)
        observed = {
            key: data[key]
            for key in _NAVIGATION_FIELDS
            if key in data
        }

        self.state.observe(
            position=observed.get("position"),
            direction=observed.get("direction"),
            attitude=observed.get("attitude"),
            horizon=observed.get("horizon"),
            uncertainty=observed.get("uncertainty"),
            evidence_cursor=(evidence.protocol_id, evidence.transition_kind),
            landscape_changed=is_transition_evidence(evidence),
        )
        return self.state

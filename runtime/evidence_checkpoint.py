"""Evidence replay from an observable Landscape checkpoint."""

from collections.abc import Iterable, Mapping

from .evidence import EvidenceRecord
from .landscape import LandscapeState


def replay_evidence_from_snapshot(
    snapshot: Mapping,
    evidence: Iterable[EvidenceRecord],
) -> LandscapeState:
    """Reconstruct state from an observable snapshot plus ordered Evidence."""
    state = LandscapeState.from_snapshot(snapshot)
    for record in evidence:
        state.apply_evidence(record)
    return state

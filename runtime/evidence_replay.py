"""Deterministic Evidence replay boundary for Runtime β0.1."""

from collections.abc import Iterable

from .evidence import EvidenceRecord
from .landscape import LandscapeState


def replay_evidence(evidence: Iterable[EvidenceRecord]) -> LandscapeState:
    """Reconstruct observable Landscape state by applying Evidence in order.

    Replay starts from an empty state and does not import external lineage,
    infer continuity, or assign semantic meaning to the evidence.
    """
    state = LandscapeState.empty()
    for record in evidence:
        state.apply_evidence(record)
    return state

"""Checkpoint plus delta execution and re-observation boundary for Runtime β0.1."""

from collections.abc import Iterable, Mapping

from .adapter import Adapter, adapt_landscape_observation
from .evidence import EvidenceRecord
from .evidence_delta import select_delta_evidence
from .landscape import LandscapeState


def execute_and_reobserve(
    snapshot: Mapping,
    evidence: Iterable[EvidenceRecord],
    applied: Iterable[EvidenceRecord],
    adapter: Adapter,
):
    """Execute unapplied Evidence from a checkpoint, then re-observe the result."""
    state = LandscapeState.from_snapshot(snapshot)
    for record in select_delta_evidence(evidence, applied):
        state.apply_evidence(record)
    return {
        "snapshot": state.snapshot(),
        "observation": adapt_landscape_observation(state),
    }

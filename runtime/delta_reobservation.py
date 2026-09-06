"""Checkpoint plus delta execution and re-observation boundary for Runtime β0.1."""

from collections.abc import Iterable, Mapping

from .adapter import Adapter
from .checkpoint_delta_execution import execute_from_checkpoint
from .evidence import EvidenceRecord


def execute_and_reobserve(
    snapshot: Mapping,
    evidence: Iterable[EvidenceRecord],
    applied: Iterable[EvidenceRecord],
    adapter: Adapter,
):
    """Execute unapplied Evidence from a checkpoint, then re-observe the result."""
    state = execute_from_checkpoint(snapshot, evidence, applied)
    return {
        "snapshot": state.snapshot(),
        "observation": adapter.adapt_landscape_observation(state),
    }

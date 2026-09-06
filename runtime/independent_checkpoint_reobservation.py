"""Independent checkpoint reconstruction and re-observation boundary."""

from collections.abc import Iterable, Mapping

from .adapter import Adapter, adapt_landscape_observation
from .evidence import EvidenceRecord
from .evidence_delta import select_delta_evidence
from .landscape import LandscapeState
from .evidence_replay import replay_evidence


def reconstruct_checkpoint(snapshot: Mapping) -> dict:
    """Create an independent observable checkpoint copy."""
    return dict(snapshot)


def reconstruct_applied_evidence(applied: Iterable[EvidenceRecord]) -> list[EvidenceRecord]:
    """Create an independent ordered container for already-applied Evidence."""
    return list(applied)


def compare_reconstructed_checkpoint(
    snapshot: Mapping,
    evidence: Iterable[EvidenceRecord],
    applied: Iterable[EvidenceRecord],
    adapter: Adapter,
):
    """Compare full replay with execution from independently reconstructed inputs."""
    records = list(evidence)
    checkpoint = reconstruct_checkpoint(snapshot)
    applied_records = reconstruct_applied_evidence(applied)
    delta = select_delta_evidence(records, applied_records)

    reconstructed_state = LandscapeState.from_snapshot(checkpoint)
    for record in delta:
        reconstructed_state.apply_evidence(record)

    full_state = replay_evidence(records)
    full_observation = adapt_landscape_observation(full_state)
    reconstructed_observation = adapt_landscape_observation(reconstructed_state)
    return {
        "full": full_observation,
        "reconstructed": reconstructed_observation,
        "equivalent": full_observation == reconstructed_observation,
    }

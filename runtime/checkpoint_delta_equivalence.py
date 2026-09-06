"""Observable equivalence check for checkpoint plus delta Evidence replay."""

from collections.abc import Iterable, Mapping

from .evidence import EvidenceRecord
from .evidence_checkpoint import replay_evidence_from_snapshot
from .evidence_delta import select_delta_evidence
from .evidence_replay import replay_evidence


def replay_checkpoint_with_delta(
    snapshot: Mapping,
    evidence: Iterable[EvidenceRecord],
    applied: Iterable[EvidenceRecord],
):
    """Reconstruct a state from a checkpoint and the unapplied Evidence delta."""
    delta = select_delta_evidence(evidence, applied)
    return replay_evidence_from_snapshot(snapshot, delta)


def equivalent_observable_state(
    evidence: Iterable[EvidenceRecord],
    snapshot: Mapping,
    applied: Iterable[EvidenceRecord],
) -> bool:
    """Return whether full replay and checkpoint-plus-delta replay match."""
    records = list(evidence)
    applied_records = list(applied)
    full_state = replay_evidence(records)
    checkpoint_state = replay_checkpoint_with_delta(
        snapshot, records, applied_records
    )
    return full_state.snapshot() == checkpoint_state.snapshot()

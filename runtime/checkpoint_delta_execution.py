"""Checkpoint plus delta Evidence execution boundary for Runtime β0.1."""

from collections.abc import Iterable, Mapping

from .evidence import EvidenceRecord
from .evidence_checkpoint import replay_evidence_from_snapshot
from .evidence_delta import select_delta_evidence


def execute_from_checkpoint(
    snapshot: Mapping,
    evidence: Iterable[EvidenceRecord],
    applied: Iterable[EvidenceRecord],
):
    """Apply only unapplied Evidence to an observable checkpoint."""
    delta = select_delta_evidence(evidence, applied)
    return replay_evidence_from_snapshot(snapshot, delta)

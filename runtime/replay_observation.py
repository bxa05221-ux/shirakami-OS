"""Read-only observation helper for Evidence replay."""

from collections.abc import Iterable, Mapping

from .evidence import EvidenceRecord
from .evidence_replay import replay_evidence


def replay_snapshot(evidence: Iterable[EvidenceRecord]) -> Mapping:
    """Return a reconstructed snapshot from ordered Evidence."""
    return replay_evidence(evidence).snapshot()

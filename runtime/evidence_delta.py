"""Read-only delta Evidence selection boundary for Runtime β0.1."""

from collections.abc import Iterable

from .evidence import EvidenceRecord


def select_delta_evidence(
    evidence: Iterable[EvidenceRecord],
    applied: Iterable[EvidenceRecord],
) -> list[EvidenceRecord]:
    """Select Evidence not already present in an applied ordered sequence."""
    applied_records = list(applied)
    return [record for record in evidence if record not in applied_records]

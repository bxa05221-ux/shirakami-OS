"""Evidence identity boundary for Runtime β0.1.

Identity is derived from the existing deterministic Evidence fingerprint. This
module does not introduce new Evidence semantics or mutate Evidence records.
"""

try:
    from .evidence import EvidenceRecord
    from .replay import evidence_fingerprint
except ImportError:  # legacy top-level runtime test imports
    from evidence import EvidenceRecord
    from replay import evidence_fingerprint


def evidence_id(evidence: EvidenceRecord) -> str:
    """Return the stable identity of an Evidence record."""
    return evidence_fingerprint(evidence)


def matches_evidence_ref(evidence: EvidenceRecord, evidence_ref: str) -> bool:
    """Check whether an Evidence record owns the supplied reference."""
    return bool(evidence_ref) and evidence_id(evidence) == evidence_ref

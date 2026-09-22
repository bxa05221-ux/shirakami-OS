"""Store bridge for immutable RunnerEvidence.

Converts RunnerEvidence through the canonical Evidence boundary and appends
the resulting records to the append-only EvidenceStore. No authority is
created or changed at this boundary.
"""

try:
    from .background_runner_evidence import RunnerEvidence
    from .evidence_store import EvidenceStore
    from .runner_evidence_bridge import runner_evidence_batch_to_evidence
except ImportError:  # legacy top-level runtime test imports
    from background_runner_evidence import RunnerEvidence
    from evidence_store import EvidenceStore
    from runner_evidence_bridge import runner_evidence_batch_to_evidence


def append_runner_evidence(
    store: EvidenceStore,
    evidence: tuple[RunnerEvidence, ...],
    *,
    protocol_id: str | None = None,
) -> EvidenceStore:
    """Convert RunnerEvidence to canonical Evidence and append it in order."""

    if not isinstance(store, EvidenceStore):
        raise TypeError("EvidenceStore is required")

    canonical = runner_evidence_batch_to_evidence(
        evidence,
        protocol_id=protocol_id,
    )
    return store.extend(canonical)

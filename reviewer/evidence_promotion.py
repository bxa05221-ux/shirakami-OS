"""Explicit Human Gate for promoting reviewer references to accepted Evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from runtime.evidence import EvidenceRecord
from runtime.evidence_store import EvidenceStore


@dataclass(frozen=True)
class EvidencePromotionRequest:
    reviewer_id: str
    evidence_ids: tuple[str, ...]
    human_gate_required: bool = True
    human_decision: str = "pending"


def promote_review_evidence(
    store: EvidenceStore,
    request: EvidencePromotionRequest,
) -> tuple[EvidenceRecord, ...]:
    """Return accepted records only after an explicit Human Gate approval.

    Reviewer-supplied IDs are references. This function never creates or mutates
    EvidenceRecord objects and never accepts a proposal as Evidence.
    """
    if request.human_gate_required is not True:
        raise ValueError("human_gate_required must remain true")
    if request.human_decision != "approved":
        raise ValueError("accepted Evidence requires explicit Human Gate approval")
    if not request.reviewer_id.strip():
        raise ValueError("reviewer_id is required")

    records = {record.evidence_id: record for record in store.all()}
    missing = [evidence_id for evidence_id in request.evidence_ids if evidence_id not in records]
    if missing:
        raise ValueError(f"unknown Evidence IDs: {', '.join(missing)}")

    return tuple(records[evidence_id] for evidence_id in request.evidence_ids)


def candidate_evidence_ids(evidence_ids: Iterable[str]) -> tuple[str, ...]:
    """Normalize reviewer references without accepting them as Evidence."""
    return tuple(dict.fromkeys(str(evidence_id) for evidence_id in evidence_ids if str(evidence_id).strip()))

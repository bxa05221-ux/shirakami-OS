"""Bridge reviewer submissions into AIwitness trace metadata without authority propagation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .registry import ReviewSubmission, ReviewerBundle


@dataclass(frozen=True)
class ReviewerTraceMetadata:
    reviewer_id: str
    evidence_ids: tuple[str, ...]
    matome_yaml: str
    trace_role: str = "review_observation"
    authority_granted: bool = False
    decision_authorized: bool = False
    human_gate_required: bool = True


def build_trace_metadata(
    bundle: ReviewerBundle,
    submission: ReviewSubmission,
) -> ReviewerTraceMetadata:
    reviewer = bundle.reviewers.get(submission.reviewer_id)
    if reviewer is None:
        raise ValueError("reviewer must be registered before trace metadata is built")
    return ReviewerTraceMetadata(
        reviewer_id=reviewer.reviewer_id,
        evidence_ids=tuple(submission.evidence_ids),
        matome_yaml=reviewer.matome_yaml,
    )


def as_trace_context(metadata: ReviewerTraceMetadata) -> dict[str, Any]:
    return {
        "reviewer_id": metadata.reviewer_id,
        "evidence_ids": list(metadata.evidence_ids),
        "matome_yaml": metadata.matome_yaml,
        "trace_role": metadata.trace_role,
        "authority_granted": metadata.authority_granted,
        "decision_authorized": metadata.decision_authorized,
        "human_gate_required": metadata.human_gate_required,
    }

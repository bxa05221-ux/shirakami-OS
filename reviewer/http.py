"""HTTP-neutral serialization helpers for the Phase 5 reviewer boundary."""

from __future__ import annotations

from typing import Any

from .registry import ReviewSubmission, Reviewer, ReviewerBundle


def register_reviewer(bundle: ReviewerBundle, payload: dict[str, Any]) -> dict[str, Any]:
    reviewer = Reviewer(
        reviewer_id=str(payload["reviewer_id"]),
        matome_yaml=str(payload["matome_yaml"]),
        metadata=payload.get("metadata", {}),
    )
    bundle.register(reviewer)
    return {"reviewer_id": reviewer.reviewer_id, "registered": True}


def submit_review(bundle: ReviewerBundle, payload: dict[str, Any]) -> dict[str, Any]:
    submission = ReviewSubmission(
        reviewer_id=str(payload["reviewer_id"]),
        observation=payload.get("observation", {}),
        evidence_ids=tuple(payload.get("evidence_ids", ())),
        proposal=payload.get("proposal", {}),
    )
    bundle.submit(submission)
    return {"reviewer_id": submission.reviewer_id, "submitted": True}


def get_reviewers(bundle: ReviewerBundle) -> dict[str, Any]:
    return bundle.comparable_view()

"""Boundary adapter for importing validated blind-review observations."""

from __future__ import annotations

from typing import Any

from .registry import ReviewSubmission, Reviewer, ReviewerBundle


def ingest_blind_review(
    bundle: ReviewerBundle,
    result: dict[str, Any],
    *,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Import a validated blind-review result without granting authority.

    The caller is responsible for validating the result with
    validate_blind_review_result before calling this adapter.
    Evidence IDs remain references and the review decision remains pending.
    """
    reviewer_id = str(result["reviewer_id"])
    matome_yaml = result.get("matome_yaml")

    if not isinstance(matome_yaml, str) or not matome_yaml.strip():
        raise ValueError("validated blind review must provide matome_yaml")

    bundle.register(
        Reviewer(
            reviewer_id=reviewer_id,
            matome_yaml=matome_yaml,
            metadata=metadata or {},
        )
    )

    observation = {
        "observations": list(result["observations"]),
        "resolved_questions": list(result["resolved_questions"]),
        "unresolved_questions": list(result["unresolved_questions"]),
        "falsifiable_points": list(result["falsifiable_points"]),
        "interpretation": list(result["interpretation"]),
    }

    submission = ReviewSubmission(
        reviewer_id=reviewer_id,
        observation=observation,
        evidence_ids=tuple(result["evidence_ids"]),
        proposal={"items": list(result["proposals"])},
    )
    bundle.submit(submission)

    return {
        "project_id": bundle.project_id,
        "reviewer_id": reviewer_id,
        "registered": True,
        "submitted": True,
        "decision": None,
        "human_gate_required": True,
        "authority_granted": False,
        "decision_authorized": False,
        "evidence_accepted": False,
    }

"""Boundary adapter for importing validated blind-review observations."""

from __future__ import annotations

from typing import Any

from scripts.validate_blind_review_result import validate_blind_review_result

from .registry import ReviewSubmission, Reviewer, ReviewerBundle


def ingest_blind_review(
    bundle: ReviewerBundle,
    result: dict[str, Any],
    *,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate and import a blind-review result without granting authority."""
    validated = validate_blind_review_result(result)
    reviewer_id = str(validated["reviewer_id"])
    matome_yaml = validated.get("matome_yaml")

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
        "observations": list(validated["observations"]),
        "resolved_questions": list(validated["resolved_questions"]),
        "unresolved_questions": list(validated["unresolved_questions"]),
        "falsifiable_points": list(validated["falsifiable_points"]),
        "interpretation": list(validated["interpretation"]),
    }

    submission = ReviewSubmission(
        reviewer_id=reviewer_id,
        observation=observation,
        evidence_ids=tuple(validated["evidence_ids"]),
        proposal={"items": list(validated["proposals"])},
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

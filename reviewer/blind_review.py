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


def ingest_and_compare_blind_reviews(
    bundle: ReviewerBundle,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate and ingest multiple blind reviews, then build a comparison context."""
    for result in results:
        ingest_blind_review(bundle, result)

    from .aiwitness_bridge import (
        as_comparative_trace_context,
        build_comparative_trace_metadata,
    )
    from .comparative_trace import build_comparative_trace

    comparative = build_comparative_trace(bundle)
    metadata = build_comparative_trace_metadata(comparative)
    return as_comparative_trace_context(metadata)

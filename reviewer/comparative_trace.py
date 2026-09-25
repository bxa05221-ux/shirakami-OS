"""Build a lossless comparative view of independent reviewer submissions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .registry import ReviewSubmission, ReviewerBundle


@dataclass(frozen=True)
class ComparativeTrace:
    project_id: str
    reviewers: tuple[dict[str, Any], ...]
    shared_evidence_ids: tuple[str, ...]
    divergent_evidence_ids: tuple[str, ...]
    observations: tuple[dict[str, Any], ...]
    human_gate_required: bool = True
    decision: None = None


def build_comparative_trace(bundle: ReviewerBundle) -> ComparativeTrace:
    evidence_by_reviewer: dict[str, set[str]] = {}
    observations: list[dict[str, Any]] = []

    for submission in bundle.submissions:
        evidence_by_reviewer.setdefault(submission.reviewer_id, set()).update(
            submission.evidence_ids
        )
        observations.append(
            {
                "reviewer_id": submission.reviewer_id,
                "observation": dict(submission.observation),
                "evidence_ids": list(submission.evidence_ids),
                "proposal": dict(submission.proposal),
            }
        )

    sets = list(evidence_by_reviewer.values())
    if len(sets) >= 2:
        shared = set.intersection(*sets)
        all_evidence = set.union(*sets)
    else:
        shared = set()
        all_evidence = set().union(*sets)

    divergent = all_evidence - shared
    reviewers = tuple(
        {
            "reviewer_id": reviewer.reviewer_id,
            "matome_yaml": reviewer.matome_yaml,
            "metadata": dict(reviewer.metadata),
        }
        for reviewer in bundle.reviewers.values()
    )

    return ComparativeTrace(
        project_id=bundle.project_id,
        reviewers=reviewers,
        shared_evidence_ids=tuple(sorted(shared)),
        divergent_evidence_ids=tuple(sorted(divergent)),
        observations=tuple(observations),
    )


def as_trace_context(trace: ComparativeTrace) -> dict[str, Any]:
    return {
        "project_id": trace.project_id,
        "reviewers": [dict(item) for item in trace.reviewers],
        "shared_evidence_ids": list(trace.shared_evidence_ids),
        "divergent_evidence_ids": list(trace.divergent_evidence_ids),
        "observations": [dict(item) for item in trace.observations],
        "human_gate_required": trace.human_gate_required,
        "decision": trace.decision,
    }

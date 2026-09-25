"""Bridge reviewer submissions into AIwitness trace metadata without authority propagation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .registry import ReviewSubmission, ReviewerBundle
from .comparative_trace import ComparativeTrace


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


@dataclass(frozen=True)
class ComparativeTraceMetadata:
    project_id: str
    reviewer_ids: tuple[str, ...]
    shared_evidence_ids: tuple[str, ...]
    divergent_evidence_ids: tuple[str, ...]
    observations: tuple[dict[str, Any], ...]
    trace_role: str = "comparative_review_observation"
    authority_granted: bool = False
    decision_authorized: bool = False
    human_gate_required: bool = True


def build_comparative_trace_metadata(
    trace: ComparativeTrace,
) -> ComparativeTraceMetadata:
    return ComparativeTraceMetadata(
        project_id=trace.project_id,
        reviewer_ids=tuple(item["reviewer_id"] for item in trace.reviewers),
        shared_evidence_ids=tuple(trace.shared_evidence_ids),
        divergent_evidence_ids=tuple(trace.divergent_evidence_ids),
        observations=tuple(dict(item) for item in trace.observations),
    )


def as_comparative_trace_context(
    metadata: ComparativeTraceMetadata,
) -> dict[str, Any]:
    return {
        "project_id": metadata.project_id,
        "reviewer_ids": list(metadata.reviewer_ids),
        "shared_evidence_ids": list(metadata.shared_evidence_ids),
        "divergent_evidence_ids": list(metadata.divergent_evidence_ids),
        "observations": [dict(item) for item in metadata.observations],
        "trace_role": metadata.trace_role,
        "authority_granted": metadata.authority_granted,
        "decision_authorized": metadata.decision_authorized,
        "decision": None,
        "human_gate_required": metadata.human_gate_required,
    }


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

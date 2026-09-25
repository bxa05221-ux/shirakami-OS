"""Multi-agent reviewer registry with human-gated aggregation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

import yaml


@dataclass(frozen=True)
class Reviewer:
    reviewer_id: str
    matome_yaml: str
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReviewSubmission:
    reviewer_id: str
    observation: Mapping[str, Any]
    evidence_ids: tuple[str, ...] = ()
    proposal: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class ReviewerBundle:
    project_id: str
    reviewers: dict[str, Reviewer] = field(default_factory=dict)
    submissions: list[ReviewSubmission] = field(default_factory=list)

    def register(self, reviewer: Reviewer) -> None:
        if not reviewer.reviewer_id.strip():
            raise ValueError("reviewer_id is required")
        if not reviewer.matome_yaml.strip():
            raise ValueError("matome_yaml is required")
        try:
            parsed = yaml.safe_load(reviewer.matome_yaml)
        except yaml.YAMLError as exc:
            raise ValueError("matome_yaml must be valid YAML") from exc
        if not isinstance(parsed, dict):
            raise ValueError("matome_yaml must contain a YAML mapping")
        if reviewer.reviewer_id in self.reviewers:
            raise ValueError(f"reviewer already registered: {reviewer.reviewer_id}")
        self.reviewers[reviewer.reviewer_id] = reviewer

    def submit(self, submission: ReviewSubmission) -> None:
        if submission.reviewer_id not in self.reviewers:
            raise ValueError("reviewer must be registered before submission")
        self.submissions.append(submission)

    def comparable_view(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "reviewers": [
                {
                    "reviewer_id": r.reviewer_id,
                    "matome_yaml": r.matome_yaml,
                    "metadata": dict(r.metadata),
                }
                for r in self.reviewers.values()
            ],
            "submissions": [
                {
                    "reviewer_id": s.reviewer_id,
                    "observation": dict(s.observation),
                    "evidence_ids": list(s.evidence_ids),
                    "proposal": dict(s.proposal),
                }
                for s in self.submissions
            ],
            "decision": None,
            "human_gate_required": True,
        }

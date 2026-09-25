"""Provider-neutral multi-agent reviewer boundary.

Reviewers emit observations and proposals; they never acquire decision authority.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True)
class ReviewerPerspective:
    reviewer_id: str
    role: str
    matome_yaml: Mapping[str, Any]
    observations: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    proposals: tuple[str, ...] = ()
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False
    human_gate_required: bool = True

    def __post_init__(self) -> None:
        if not self.reviewer_id or not self.role:
            raise ValueError("reviewer identity must be non-empty")
        if self.execution_authorized or self.publish_authorized or self.merge_authorized:
            raise ValueError("reviewer cannot grant authority")
        if not self.human_gate_required:
            raise ValueError("human_gate_required must remain true")

@dataclass(frozen=True)
class ReviewerBundle:
    project: str
    objective: str
    reviewers: tuple[ReviewerPerspective, ...] = field(default_factory=tuple)
    evidence_ids: tuple[str, ...] = ()
    human_gate_required: bool = True

    def __post_init__(self) -> None:
        if not self.project or not self.objective:
            raise ValueError("project and objective are required")
        if not self.human_gate_required:
            raise ValueError("human_gate_required must remain true")

    def compare(self) -> dict[str, Any]:
        """Return comparable observations without producing consensus or a decision."""
        return {
            "project": self.project,
            "objective": self.objective,
            "reviewers": [
                {
                    "reviewer_id": item.reviewer_id,
                    "role": item.role,
                    "matome_yaml": dict(item.matome_yaml),
                    "observations": list(item.observations),
                    "evidence_ids": list(item.evidence_ids),
                    "proposals": list(item.proposals),
                    "execution_authorized": False,
                    "publish_authorized": False,
                    "merge_authorized": False,
                    "human_gate_required": True,
                }
                for item in self.reviewers
            ],
            "evidence_ids": list(self.evidence_ids),
            "human_gate_required": True,
            "decision": None,
        }

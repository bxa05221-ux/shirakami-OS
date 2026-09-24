"""Minimal Decision lineage boundary for Runtime handoff v0.1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionLineage:
    """Historical relation between a decision and the decision it supersedes."""

    decision_id: str
    timestamp: str
    supersedes: str | None = None

    def __post_init__(self) -> None:
        if not self.decision_id:
            raise ValueError("decision_id must not be empty")
        if not self.timestamp:
            raise ValueError("timestamp must not be empty")
        if self.supersedes == self.decision_id:
            raise ValueError("decision cannot supersede itself")

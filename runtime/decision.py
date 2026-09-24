"""Minimal Decision boundary for Runtime research handoff v0.1.

A Decision records an explicit choice about an Interpretation.
Human authority is validated by the HumanGate boundary rather than inferred
from actor_id naming conventions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json


@dataclass(frozen=True)
class DecisionRecord:
    """An immutable decision targeting an InterpretationRecord."""

    actor_id: str
    target_interpretation_id: str
    timestamp: str
    supersedes: str | None = None
    decision_id: str = field(init=False)

    def __post_init__(self) -> None:
        if not self.actor_id:
            raise ValueError("actor_id must not be empty")
        if not self.target_interpretation_id:
            raise ValueError("target_interpretation_id must not be empty")
        if not self.timestamp:
            raise ValueError("timestamp must not be empty")

        canonical = json.dumps(
            {
                "actor_id": self.actor_id,
                "target_interpretation_id": self.target_interpretation_id,
                "timestamp": self.timestamp,
                "supersedes": self.supersedes,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        object.__setattr__(self, "decision_id", hashlib.sha256(canonical).hexdigest())

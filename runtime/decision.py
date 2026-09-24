"""Minimal human-authorized Decision boundary for Shirakami Runtime β0.1."""

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class DecisionRecord:
    """A human decision referring to an InterpretationRecord.

    Presence of an Actor never implies authority; the Runtime records the
    declared human actor explicitly and never promotes an Interpretation to a
    Decision implicitly.
    """

    actor_id: str
    target: str
    content: Mapping[str, Any]
    timestamp: str
    supersedes: str | None = None
    decision_id: str = field(init=False)

    def __post_init__(self) -> None:
        canonical = json.dumps(
            {
                "actor_id": self.actor_id,
                "target": self.target,
                "content": self.content,
                "timestamp": self.timestamp,
                "supersedes": self.supersedes,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")
        object.__setattr__(self, "decision_id", hashlib.sha256(canonical).hexdigest())

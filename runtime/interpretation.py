"""Minimal attributable Interpretation boundary for Runtime β0.1.

Interpretations are proposals derived from Evidence. They never carry decision
authority and remain independently identifiable by a stable interpretation_id.
"""

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class InterpretationRecord:
    """An attributable interpretation of one or more Evidence records."""

    source_evidence: tuple[str, ...]
    actor_id: str
    content: Mapping[str, Any]
    status: str = "proposed"
    interpretation_id: str = field(init=False)

    def __post_init__(self) -> None:
        canonical = json.dumps(
            {
                "source_evidence": self.source_evidence,
                "actor_id": self.actor_id,
                "content": self.content,
                "status": self.status,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")
        object.__setattr__(
            self,
            "interpretation_id",
            hashlib.sha256(canonical).hexdigest(),
        )

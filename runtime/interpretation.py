"""Minimal attributed Interpretation boundary for Runtime research handoff v0.1.

This module intentionally does not create authority or mutate Evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


_ALLOWED_STATUS = frozenset({"proposed", "accepted", "rejected", "superseded"})


@dataclass(frozen=True)
class InterpretationRecord:
    """An attributed interpretation derived from stable Evidence references."""

    actor_id: str
    source_evidence_ids: Tuple[str, ...]
    content: str
    status: str = "proposed"
    interpretation_id: str = field(init=False)

    def __post_init__(self) -> None:
        if not self.actor_id:
            raise ValueError("actor_id must not be empty")
        if not self.source_evidence_ids:
            raise ValueError("source_evidence_ids must not be empty")
        if not self.content:
            raise ValueError("content must not be empty")
        if self.status not in _ALLOWED_STATUS:
            raise ValueError(f"unsupported interpretation status: {self.status}")

        # Identity is deterministic but intentionally distinct from Evidence.
        import hashlib
        import json

        canonical = json.dumps(
            {
                "actor_id": self.actor_id,
                "source_evidence_ids": self.source_evidence_ids,
                "content": self.content,
                "status": self.status,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        object.__setattr__(
            self,
            "interpretation_id",
            hashlib.sha256(canonical).hexdigest(),
        )

    @property
    def is_authority(self) -> bool:
        """Interpretation never constitutes Human Gate authority."""
        return False

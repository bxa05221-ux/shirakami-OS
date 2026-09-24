"""Canonical SemanticHandoff envelope for the external Shirakami API."""

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class SemanticHandoff:
    """Transport a verified semantic lineage without granting new authority."""

    evidence_ids: tuple[str, ...]
    interpretation_id: str | None
    decision_id: str | None
    gate_id: str | None
    payload: Mapping[str, Any]
    handoff_id: str = field(init=False)

    def __post_init__(self) -> None:
        canonical = json.dumps(
            {
                "evidence_ids": self.evidence_ids,
                "interpretation_id": self.interpretation_id,
                "decision_id": self.decision_id,
                "gate_id": self.gate_id,
                "payload": self.payload,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")
        object.__setattr__(self, "handoff_id", hashlib.sha256(canonical).hexdigest())

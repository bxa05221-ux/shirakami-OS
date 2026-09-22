"""Minimal immutable Evidence boundary for Runtime β0.1."""

from dataclasses import dataclass, field
import hashlib
import json
from types import MappingProxyType
from typing import Any, Mapping

try:
    from .prototype import ExecutionResult
except ImportError:
    from prototype import ExecutionResult


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable record of an observed Runtime transition.

    evidence_id is content-addressed identity. It identifies the Evidence
    payload; it does not identify an occurrence and it grants no authority.
    """

    protocol_id: str
    status: str
    transition_kind: str
    transition_data: Mapping[str, Any]
    signals: tuple[str, ...]
    confidence: str = "observed"
    evidence_id: str = field(init=False)

    def __post_init__(self) -> None:
        canonical = json.dumps(
            {
                "protocol_id": self.protocol_id,
                "status": self.status,
                "transition_kind": self.transition_kind,
                "transition_data": self.transition_data,
                "signals": self.signals,
                "confidence": self.confidence,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")
        object.__setattr__(self, "evidence_id", hashlib.sha256(canonical).hexdigest())

    @classmethod
    def from_result(cls, result: ExecutionResult) -> "EvidenceRecord":
        return cls(
            protocol_id=result.protocol_id,
            status=result.status,
            transition_kind=result.transition.kind,
            transition_data=MappingProxyType(dict(result.transition.data)),
            signals=tuple(result.signals),
        )


def capture_evidence(result: ExecutionResult) -> EvidenceRecord:
    return EvidenceRecord.from_result(result)


def is_transition_evidence(evidence: EvidenceRecord) -> bool:
    return bool(evidence.transition_kind and evidence.transition_data.get("changed"))

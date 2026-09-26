"""Minimal immutable Evidence boundary for Runtime β0.1."""

from dataclasses import dataclass, field
import hashlib
import json
from types import MappingProxyType
from typing import Any, Mapping

try:
    from .prototype import ExecutionResult
except ImportError:  # legacy top-level runtime test imports
    from prototype import ExecutionResult


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable record of an observed Runtime transition."""

    protocol_id: str
    status: str
    transition_kind: str
    transition_data: Mapping[str, Any]
    signals: tuple[str, ...]
    confidence: str = "observed"
    evidence_id: str = field(init=False)
    _model_output: Any | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        canonical = json.dumps(
            {
                "protocol_id": self.protocol_id,
                "status": self.status,
                "transition_kind": self.transition_kind,
                "transition_data": self.transition_data,
                "signals": self.signals,
                "confidence": self.confidence,
                "model_output": self._model_output,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")
        object.__setattr__(self, "evidence_id", hashlib.sha256(canonical).hexdigest())

    @classmethod
    def from_result(
        cls,
        result: ExecutionResult,
        *,
        model_output: Any | None = None,
    ) -> "EvidenceRecord":
        record = cls(
            protocol_id=result.protocol_id,
            status=result.status,
            transition_kind=result.transition.kind,
            transition_data=MappingProxyType(dict(result.transition.data)),
            signals=tuple(result.signals),
        )
        object.__setattr__(record, "_model_output", model_output)
        canonical = json.dumps(
            {
                "protocol_id": record.protocol_id,
                "status": record.status,
                "transition_kind": record.transition_kind,
                "transition_data": record.transition_data,
                "signals": record.signals,
                "confidence": record.confidence,
                "model_output": model_output,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")
        object.__setattr__(record, "evidence_id", hashlib.sha256(canonical).hexdigest())
        return record

    @property
    def model_output(self) -> Any | None:
        return self._model_output


def capture_evidence(
    result: ExecutionResult,
    *,
    model_output: Any | None = None,
) -> EvidenceRecord:
    return EvidenceRecord.from_result(result, model_output=model_output)


def is_transition_evidence(evidence: EvidenceRecord) -> bool:
    return bool(evidence.transition_kind and evidence.transition_data.get("changed"))

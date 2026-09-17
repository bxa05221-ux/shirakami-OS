"""Minimal immutable Evidence boundary for Runtime β0.1."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

try:
    from .prototype import ExecutionResult
except ImportError:  # legacy top-level runtime test imports
    from prototype import ExecutionResult


def _freeze(value: Any) -> Any:
    """Recursively freeze common mutable container values."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, set):
        return frozenset(_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable record of an observed Runtime transition."""

    protocol_id: str
    status: str
    transition_kind: str
    transition_data: Mapping[str, Any]
    signals: tuple[str, ...]
    confidence: str = "observed"

    @classmethod
    def from_result(cls, result: ExecutionResult) -> "EvidenceRecord":
        return cls(
            protocol_id=result.protocol_id,
            status=result.status,
            transition_kind=result.transition.kind,
            transition_data=_freeze(result.transition.data),
            signals=tuple(result.signals),
        )


def capture_evidence(result: ExecutionResult) -> EvidenceRecord:
    return EvidenceRecord.from_result(result)


def is_transition_evidence(evidence: EvidenceRecord) -> bool:
    return bool(evidence.transition_kind and evidence.transition_data.get("changed"))

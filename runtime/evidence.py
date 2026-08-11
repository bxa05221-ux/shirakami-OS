"""Minimal immutable Evidence boundary for Runtime β0.1."""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from prototype import ExecutionResult, Transition


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable record of an observed Runtime transition."""

    protocol_id: str
    status: str
    transition_kind: str
    transition_data: Mapping[str, Any]
    signals: tuple[str, ...]

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
    """Capture evidence at the execution-result/transition boundary."""

    return EvidenceRecord.from_result(result)


def is_transition_evidence(evidence: EvidenceRecord) -> bool:
    return bool(evidence.transition_kind and evidence.transition_data.get("changed"))

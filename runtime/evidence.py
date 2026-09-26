"""Minimal immutable Evidence boundary for Runtime β0.1."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

try:
    from .prototype import ExecutionResult
except ImportError:  # legacy top-level runtime test imports
    from prototype import ExecutionResult


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable record of an observed Runtime transition and model output."""

    protocol_id: str
    status: str
    transition_kind: str
    transition_data: Mapping[str, Any]
    signals: tuple[str, ...]
    confidence: str = "observed"
    _model_output: Any | None = field(default=None, init=False, repr=False)

    @property
    def model_output(self) -> Any | None:
        """Return model output without changing the public record constructor shape."""
        return self._model_output

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
        return record


def capture_evidence(
    result: ExecutionResult,
    *,
    model_output: Any | None = None,
) -> EvidenceRecord:
    return EvidenceRecord.from_result(result, model_output=model_output)


def is_transition_evidence(evidence: EvidenceRecord) -> bool:
    return bool(evidence.transition_kind and evidence.transition_data.get("changed"))

"""Backend-agnostic Adapter boundaries for Runtime β0.1.

Adapters expose external boundaries without embedding backend-specific
semantics in the Runtime Kernel.
"""

from typing import Any, Mapping, Protocol

try:
    from .landscape import LandscapeState
except ImportError:  # legacy top-level runtime imports
    from landscape import LandscapeState


class Adapter(Protocol):
    """Conceptual external-backend input boundary."""

    def read(self, reference: str) -> Mapping[str, Any]:
        ...


class MemoryAdapter:
    """Deterministic in-memory adapter used for boundary verification."""

    def __init__(self, records: Mapping[str, Mapping[str, Any]] | None = None):
        self._records = dict(records or {})

    def read(self, reference: str) -> Mapping[str, Any]:
        if reference not in self._records:
            raise KeyError(reference)
        return dict(self._records[reference])


def adapt_landscape_observation(state: LandscapeState) -> Mapping[str, Any]:
    """Expose observable Landscape state without semantic interpretation."""
    evidence_lineage = tuple(
        {
            "protocol_id": evidence.protocol_id,
            "status": evidence.status,
            "transition_kind": evidence.transition_kind,
            "transition_data": dict(evidence.transition_data),
            "signals": tuple(evidence.signals),
            "confidence": evidence.confidence,
        }
        for evidence in state.evidence
    )
    return {
        "snapshot": state.snapshot(),
        "evidence_lineage": evidence_lineage,
    }

class AdapterExecutionError(ValueError):
    """Raised when a Pipeline step cannot cross the Adapter boundary."""


@dataclass(frozen=True)
class PipelineAdapterRequest:
    protocol_id: str
    version: str
    phase: str
    action: str
    input: Mapping[str, Any]
    context: Mapping[str, Any]


@dataclass(frozen=True)
class PipelineAdapterResult:
    output: Any
    backend: str | None
    evidence: Mapping[str, Any]


class PipelineAdapter:
    """Replaceable boundary from a Pipeline step to an external backend."""

    def __init__(self, backend: Callable[[PipelineAdapterRequest], Any], backend_id: str | None = None):
        if not callable(backend):
            raise AdapterExecutionError("backend must be callable")
        self._backend = backend
        self.backend_id = backend_id

    def execute(self, request: PipelineAdapterRequest) -> PipelineAdapterResult:
        for field in ("protocol_id", "version", "phase", "action"):
            if not getattr(request, field):
                raise AdapterExecutionError(f"{field} is required")
        output = self._backend(request)
        return PipelineAdapterResult(
            output=output,
            backend=self.backend_id,
            evidence={
                "event": "adapter.pipeline_execution",
                "protocol_id": request.protocol_id,
                "version": request.version,
                "phase": request.phase,
                "action": request.action,
                "backend_declared": self.backend_id is not None,
            },
        )

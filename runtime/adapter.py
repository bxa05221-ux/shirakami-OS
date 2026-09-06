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

    def adapt_landscape_observation(self, state: LandscapeState) -> Mapping[str, Any]:
        """Compatibility method delegating to the existing observation boundary."""
        return adapt_landscape_observation(state)


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

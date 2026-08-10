"""Minimal Adapter boundary for Runtime β0.1.

The Adapter is deliberately backend-agnostic. It exposes only the boundary
needed by the Runtime prototype: obtaining external input without embedding
backend-specific behavior in Runtime.
"""

from typing import Any, Mapping, Protocol


class Adapter(Protocol):
    """Conceptual external-backend boundary."""

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

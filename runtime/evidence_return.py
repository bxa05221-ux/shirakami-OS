"""Compatibility boundary for Adapter/Backend response to Evidence conversion."""

from __future__ import annotations

try:
    from .evidence_return_backend import evidence_from_backend_response
except ImportError:
    from evidence_return_backend import evidence_from_backend_response


def evidence_from_adapter_response(response, *, protocol_id: str = "adapter.return.v0.1"):
    """Record an adapter/backend response as observed Evidence."""
    return evidence_from_backend_response(response, protocol_id=protocol_id)


__all__ = ["evidence_from_adapter_response", "evidence_from_backend_response"]

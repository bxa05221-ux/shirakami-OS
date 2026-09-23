"""Compatibility boundary for Adapter/Backend response to Evidence conversion."""

from __future__ import annotations

try:
    from .evidence_return_backend import evidence_from_backend_response
    from .evidence import EvidenceRecord
except ImportError:
    from evidence_return_backend import evidence_from_backend_response
    from evidence import EvidenceRecord


def evidence_from_adapter_response(response, *, protocol_id: str = "adapter.return.v0.1") -> EvidenceRecord:
    """Record an adapter response as observed Evidence without inferring backend identity."""
    return EvidenceRecord(
        protocol_id=protocol_id,
        status=response.status,
        transition_kind="adapter.response",
        transition_data={
            "adapter_id": response.adapter_id,
            "payload": dict(response.payload),
            "authority": "not_inferred",
        },
        signals=("adapter.response.received",),
        confidence="observed",
    )


__all__ = ["evidence_from_adapter_response", "evidence_from_backend_response"]

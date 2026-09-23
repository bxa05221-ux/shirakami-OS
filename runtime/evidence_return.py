"""Convert an AdapterResponse into immutable Runtime Evidence."""

from __future__ import annotations

from typing import Any

from .adapter import AdapterResponse
from .evidence import EvidenceRecord


def evidence_from_adapter_response(
    response: AdapterResponse,
    *,
    protocol_id: str = "adapter.return.v0.1",
) -> EvidenceRecord:
    """Record an external Adapter result without inferring authority."""
    return EvidenceRecord(
        protocol_id=protocol_id,
        status=response.status,
        transition_kind="adapter.response",
        transition_data={
            "adapter_id": response.adapter_id,
            "payload": dict(response.payload),
            "authority": response.evidence.get("authority", "not_inferred"),
        },
        signals=("adapter.response.received",),
        confidence="observed",
    )

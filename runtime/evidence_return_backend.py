"""Convert a BackendResponse into immutable Runtime Evidence."""

from __future__ import annotations

from typing import Any, Mapping

try:
    from .backend import BackendResponse
    from .evidence import EvidenceRecord
except ImportError:
    from backend import BackendResponse
    from evidence import EvidenceRecord


def evidence_from_backend_response(
    response: BackendResponse,
    *,
    protocol_id: str = "backend.return.v0.1",
    context_lineage: Mapping[str, Any] | None = None,
) -> EvidenceRecord:
    """Record backend output as observed data; never infer authority."""
    transition_data = {
        "backend_id": response.backend_id,
        "payload": dict(response.payload),
        "authority": "not_inferred",
    }
    if context_lineage is not None:
        transition_data["context_lineage"] = dict(context_lineage)
    return EvidenceRecord(
        protocol_id=protocol_id,
        status=response.status,
        transition_kind="backend.response",
        transition_data=transition_data,
        signals=("backend.response.received",),
        confidence="observed",
    )

"""Return BackendResponse to immutable EvidenceRecord."""

from .backend import BackendResponse
from .evidence import EvidenceRecord


def evidence_from_backend_response(
    response: BackendResponse,
    *,
    protocol_id: str = "backend.return.v0.1",
) -> EvidenceRecord:
    """Record backend output as observed data, never as a Decision."""
    return EvidenceRecord(
        protocol_id=protocol_id,
        status=response.status,
        transition_kind="backend.response",
        transition_data={
            "backend_id": response.backend_id,
            "payload": dict(response.payload),
            "authority": "not_inferred",
        },
        signals=("backend.response.received",),
        confidence="observed",
    )

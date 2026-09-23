"""Minimal end-to-end Evolution Loop proof using the reference backend."""

from runtime.backend import EchoBackend
from runtime.backend_evidence import evidence_from_backend_response
from runtime.evidence_return import evidence_from_adapter_response


def test_adapter_backend_evidence_loop_closes_without_authority_inference():
    handoff = {
        "handoff_id": "h-loop-001",
        "evidence_ids": ["e-001"],
        "interpretation_id": "i-001",
        "decision_id": "d-001",
        "gate_id": "g-001",
        "payload": {"task": "round-trip"},
        "authority": "not_inferred",
    }

    backend_response = EchoBackend().execute(handoff)
    backend_evidence = evidence_from_backend_response(backend_response)

    assert backend_evidence.status == "completed"
    assert backend_evidence.transition_data["authority"] == "not_inferred"
    assert backend_evidence.evidence_id

    # The same evidence shape is accepted by the existing Adapter-return boundary.
    adapter_like = type("AdapterLike", (), {
        "adapter_id": backend_response.backend_id,
        "status": backend_response.status,
        "payload": backend_response.payload,
        "evidence": {"authority": "not_inferred"},
    })()
    adapter_evidence = evidence_from_adapter_response(adapter_like)
    assert adapter_evidence.transition_data["authority"] == "not_inferred"

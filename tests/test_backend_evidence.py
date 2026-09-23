"""Backend -> Evidence boundary tests."""

from runtime.backend import EchoBackend
from runtime.backend_evidence import evidence_from_backend_response


def test_backend_response_becomes_observed_evidence():
    response = EchoBackend().execute({"handoff_id": "h-001", "payload": {"x": 1}})
    evidence = evidence_from_backend_response(response)

    assert evidence.transition_kind == "backend.response"
    assert evidence.transition_data["backend_id"] == "echo-backend:v0.1"
    assert evidence.transition_data["authority"] == "not_inferred"
    assert evidence.transition_data["payload"]["echo"]["handoff_id"] == "h-001"
    assert evidence.signals == ("backend.response.received",)


def test_backend_response_evidence_identity_is_stable():
    response = EchoBackend().execute({"handoff_id": "h-002", "payload": {"x": 1}})
    first = evidence_from_backend_response(response)
    second = evidence_from_backend_response(response)
    assert first.evidence_id == second.evidence_id

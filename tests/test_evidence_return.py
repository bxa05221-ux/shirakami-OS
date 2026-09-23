"""Tests for the Adapter -> Evidence return boundary."""

from runtime.adapter import EchoAdapter
from runtime.evidence_return import evidence_from_adapter_response


def test_adapter_response_returns_as_observed_evidence():
    handoff = {
        "handoff_id": "h-001",
        "evidence_ids": ["e-001"],
        "interpretation_id": "i-001",
        "decision_id": "d-001",
        "gate_id": "g-001",
        "payload": {"value": "hello"},
        "authority": "not_inferred",
    }
    response = EchoAdapter().emit(handoff)
    evidence = evidence_from_adapter_response(response)

    assert evidence.status == "completed"
    assert evidence.transition_kind == "adapter.response"
    assert evidence.transition_data["adapter_id"] == "echo:v0.1"
    assert evidence.transition_data["payload"]["echo"] == handoff
    assert evidence.transition_data["authority"] == "not_inferred"
    assert evidence.signals == ("adapter.response.received",)
    assert evidence.evidence_id


def test_same_adapter_response_produces_stable_evidence_identity():
    response = EchoAdapter().emit({"handoff_id": "h-002", "payload": {"x": 1}})
    first = evidence_from_adapter_response(response)
    second = evidence_from_adapter_response(response)
    assert first == second
    assert first.evidence_id == second.evidence_id

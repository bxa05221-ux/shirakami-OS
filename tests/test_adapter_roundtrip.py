"""Round-trip contract tests for the vendor-neutral Adapter boundary."""

from runtime.adapter import EchoAdapter


def test_echo_adapter_preserves_handoff_and_never_infers_authority():
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

    assert response.status == "completed"
    assert response.adapter_id == "echo:v0.1"
    assert response.payload["echo"] == handoff
    assert response.evidence["authority"] == "not_inferred"
    assert response.evidence["adapter_id"] == "echo:v0.1"


def test_echo_adapter_is_deterministic_for_same_handoff():
    handoff = {"handoff_id": "h-002", "payload": {"x": 1}}
    first = EchoAdapter().emit(handoff)
    second = EchoAdapter().emit(handoff)
    assert first == second

"""Contract tests for the vendor-neutral SemanticHandoff Adapter boundary."""

from runtime.adapter import EchoAdapter


def test_echo_adapter_returns_transport_evidence_without_authority():
    handoff = {
        "handoff_id": "h-001",
        "evidence_ids": ["e-001"],
        "interpretation_id": "i-001",
        "decision_id": "d-001",
        "gate_id": "g-001",
        "payload": {"value": "hello"},
    }

    result = EchoAdapter().emit(handoff)

    assert result.adapter_id == "echo:v0.1"
    assert result.status == "completed"
    assert result.payload["echo"] == handoff
    assert result.evidence["authority"] == "not_inferred"
    assert result.evidence["operation"] == "adapter.emit"

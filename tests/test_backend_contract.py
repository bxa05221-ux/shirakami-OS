"""Contract tests for replaceable Backend implementations."""

from runtime.backend import EchoBackend


def test_echo_backend_returns_data_without_authority():
    handoff = {"handoff_id": "h-001", "payload": {"value": "hello"}}
    response = EchoBackend().execute(handoff)

    assert response.backend_id == "echo-backend:v0.1"
    assert response.status == "completed"
    assert response.payload["echo"] == handoff
    assert "authority" not in response.payload

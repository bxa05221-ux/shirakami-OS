from api.evolution_v0_1 import execute_evolution_v0_1
from runtime.backend import BackendResponse


class DummyBackend:
    def execute(self, handoff):
        return BackendResponse(
            backend_id="dummy",
            status="ok",
            payload={"echo": dict(handoff)},
        )


def test_evolution_api_v0_1_returns_evidence():
    result = execute_evolution_v0_1(
        DummyBackend(),
        {"handoff_id": "h-001", "authorized": True},
    )

    assert result["protocol_id"] == "evolution-loop.v0.1"
    assert result["transition_kind"] == "backend.response"
    assert result["confidence"] == "observed"
    assert result["transition_data"]["authority"] == "not_inferred"
    assert result["transition_data"]["backend_id"] == "dummy"

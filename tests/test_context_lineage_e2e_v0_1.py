from api.evolution_v0_1 import execute_evolution_v0_1
from runtime.backend import BackendResponse


class LineageBackend:
    def execute(self, handoff):
        return BackendResponse(
            backend_id="lineage-dummy",
            status="ok",
            payload={"observed_request_id": handoff["request_id"]},
        )


def test_context_lineage_survives_to_final_evidence():
    request_id = "req-e2e-001"
    result = execute_evolution_v0_1(
        LineageBackend(),
        {
            "handoff_id": "h-e2e-001",
            "request_id": request_id,
            "authorized": True,
            "evidence_ids": ["e-002", "e-001"],
            "protocol_ids": ["p-001"],
            "runtime_ids": ["r-001"],
            "evidence_store": {
                "e-001": {"value": "first"},
                "e-002": {"value": "second"},
                "e-999": {"value": "must-not-enter"},
            },
        },
    )

    evidence = result
    lineage = evidence["transition_data"]["context_lineage"]

    assert lineage == {
        "request_id": request_id,
        "evidence_ids": ["e-002", "e-001"],
        "protocol_ids": ["p-001"],
        "runtime_ids": ["r-001"],
    }
    assert evidence["transition_data"]["authority"] == "not_inferred"
    assert evidence["transition_kind"] == "backend.response"

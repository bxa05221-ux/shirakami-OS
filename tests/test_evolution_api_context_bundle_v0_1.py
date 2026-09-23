from api.evolution_v0_1 import execute_evolution_v0_1
from runtime.backend import BackendResponse


class DummyBackend:
    def execute(self, handoff):
        return BackendResponse(
            backend_id="dummy",
            status="ok",
            payload={"echo": dict(handoff)},
        )


def test_evolution_api_admits_only_explicit_context_bundle():
    result = execute_evolution_v0_1(
        DummyBackend(),
        {
            "handoff_id": "h-ctx-001",
            "request_id": "req-ctx-001",
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

    echoed = result["transition_data"]["payload"]["echo"]
    assert echoed["context_bundle"]["request_id"] == "req-ctx-001"
    assert [x["evidence_id"] for x in echoed["context_bundle"]["evidence"]] == [
        "e-002",
        "e-001",
    ]
    assert "e-999" not in str(echoed["context_bundle"])
    assert "evidence_store" not in echoed
    assert echoed["context_lineage"] == {\n        "request_id": "req-ctx-001",\n        "evidence_ids": ["e-002", "e-001"],\n        "protocol_ids": ["p-001"],\n        "runtime_ids": ["r-001"],\n    }

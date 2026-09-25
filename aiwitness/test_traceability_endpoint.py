from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from api.http import create_app
from runtime.api import ShirakamiAPI
from runtime.evolution_pipeline import EvidenceDrivenRuntime
from runtime.prototype import Transition


def _protocol(_: Any) -> Transition:
    return Transition(kind="endpoint.traceability", data={"changed": True})


def test_traceability_endpoint_returns_valid_chain() -> None:
    api = ShirakamiAPI(EvidenceDrivenRuntime())
    api.observe({}, __import__("runtime.evolution_bridge", fromlist=["ContextSnapshot"]).ContextSnapshot(protocol_id="endpoint.traceability", landscape={}, metadata={}))
    api.analyze("endpoint.traceability", protocol_exists=True)
    app = create_app(api, {"endpoint.traceability": _protocol})
    client = TestClient(app)

    response = client.post("/v1/execute", json={
        "protocol_id": "endpoint.traceability",
        "input_data": {},
        "handoff_id": "SH-HO-ENDPOINT-001",
        "evidence_ids": ["E-ENDPOINT-1"],
        "boundary_context": {
            "handoff_id": "SH-HO-ENDPOINT-001",
            "project": "Shirakami",
            "objective": "traceability endpoint",
            "protocol_ids": ["endpoint.traceability"],
            "evidence_ids": ["E-ENDPOINT-1"],
            "verification_scope": ["endpoint"],
        },
    })
    assert response.status_code == 200
    body = response.json()

    result = client.get(f"/v1/traceability/{body['trace_id']}")
    assert result.status_code == 200
    payload = result.json()
    assert payload["valid"] is True
    assert payload["traceability"]["trace_id"] == body["trace_id"]
    assert payload["traceability"]["execution_authorized"] is False
    assert payload["traceability"]["human_gate_required"] is True

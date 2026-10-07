from fastapi.testclient import TestClient

from api.http import create_app
from runtime.prototype import Transition

API_KEY = "test-shirakami-key"

def echo_protocol(input_data):
    return Transition(kind="api.mvp.async-provider-fixture", data={"output": dict(input_data.input)})

def test_async_http_provider_output_crosses_evidence_trace_and_authority_boundary():
    async def provider(prompt, protocol_id):
        return {"output": f"external:{prompt}", "provider": "async-fixture", "protocol_id": protocol_id}

    client = TestClient(create_app(protocol_registry={"fixture.async-provider": echo_protocol}, api_key=API_KEY, async_model_adapter=provider))
    payload = {
        "protocol_id": "fixture.async-provider",
        "input_data": {"text": "async external provider"},
        "handoff_id": "SH-HO-ASYNC-001",
        "trace_id": "TRACE-ASYNC-001",
        "evidence_ids": [],
        "boundary_context": {
            "handoff_id": "SH-HO-ASYNC-001",
            "project": "Shirakami API MVP",
            "objective": "Verify async external provider output crosses the complete evidence boundary",
            "protocol_ids": ["fixture.async-provider"],
            "evidence_ids": [],
            "verification_scope": ["HTTP", "async provider", "RuntimeResult", "Evidence", "Trace", "AIwitness"],
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }
    response = client.post("/v1/execute", json=payload, headers={"X-API-Key": API_KEY})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["model_output"]["output"] == "external:async external provider"
    assert body["model_output"]["provider"] == "async-fixture"
    assert body["execution_authorized"] is False
    assert body["human_gate_required"] is True
    evidence_id = body["evidence_ids"][0]
    evidence = client.get(f"/v1/evidence/{evidence_id}", headers={"X-API-Key": API_KEY})
    trace = client.get("/v1/traces/TRACE-ASYNC-001", headers={"X-API-Key": API_KEY})
    witness = client.get("/v1/witnesses/TRACE-ASYNC-001", headers={"X-API-Key": API_KEY})
    traceability = client.get("/v1/traceability/TRACE-ASYNC-001", headers={"X-API-Key": API_KEY})
    assert evidence.status_code == 200
    assert trace.status_code == 200
    assert witness.status_code == 200
    assert traceability.status_code == 200
    assert evidence.json()["model_output"] == body["model_output"]
    assert trace.json()["evidence_ids"] == [evidence_id]
    assert witness.json()["evidence_ids"] == [evidence_id]
    assert traceability.json()["valid"] is True

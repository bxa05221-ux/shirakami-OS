from fastapi.testclient import TestClient

from api.http import create_app
from runtime.prototype import Transition
from runtime.real_model_adapter import RealModelAdapter, fixture_transport


API_KEY = "test-shirakami-key"


def echo_protocol(input_data):
    return Transition(
        kind="api.mvp.real-model-fixture",
        data={"output": dict(input_data.input)},
    )


def test_http_real_model_adapter_crosses_evidence_trace_and_aiwitness():
    adapter = RealModelAdapter(fixture_transport)
    client = TestClient(
        create_app(
            protocol_registry={"fixture.real-model": echo_protocol},
            api_key=API_KEY,
            model_adapter=adapter,
        )
    )

    payload = {
        "protocol_id": "fixture.real-model",
        "input_data": {"text": "HTTP real model boundary"},
        "handoff_id": "SH-HO-REAL-MODEL-001",
        "trace_id": "TRACE-REAL-MODEL-001",
        "evidence_ids": [],
        "boundary_context": {
            "handoff_id": "SH-HO-REAL-MODEL-001",
            "project": "Shirakami API MVP",
            "objective": "Verify HTTP to replaceable real-model boundary",
            "protocol_ids": ["fixture.real-model"],
            "evidence_ids": [],
            "verification_scope": ["HTTP", "model adapter", "Evidence", "Trace", "AIwitness"],
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }

    response = client.post(
        "/v1/execute",
        json=payload,
        headers={"X-API-Key": API_KEY},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "completed"
    assert body["model_output"]["output"] == "HTTP real model boundary"
    assert body["model_output"]["provider"] == "fixture"
    assert body["execution_authorized"] is False
    assert body["human_gate_required"] is True
    assert body["evidence_ids"]

    evidence_id = body["evidence_ids"][0]
    evidence = client.get(
        f"/v1/evidence/{evidence_id}",
        headers={"X-API-Key": API_KEY},
    )
    trace = client.get(
        "/v1/traces/TRACE-REAL-MODEL-001",
        headers={"X-API-Key": API_KEY},
    )
    witness = client.get(
        "/v1/witnesses/TRACE-REAL-MODEL-001",
        headers={"X-API-Key": API_KEY},
    )
    traceability = client.get(
        "/v1/traceability/TRACE-REAL-MODEL-001",
        headers={"X-API-Key": API_KEY},
    )

    assert evidence.status_code == 200
    assert trace.status_code == 200
    assert witness.status_code == 200
    assert traceability.status_code == 200

    assert evidence.json()["model_output"] == body["model_output"]
    assert trace.json()["evidence_ids"] == [evidence_id]
    assert witness.json()["evidence_ids"] == [evidence_id]
    assert traceability.json()["valid"] is True

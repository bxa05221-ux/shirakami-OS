from fastapi.testclient import TestClient

from api.http import create_app
from runtime.prototype import Transition


API_KEY = "test-shirakami-key"


def echo_protocol(input_data):
    return Transition(
        kind="api.mvp.fixture",
        data={"output": dict(input_data or {})},
    )


def test_keyless_provider_neutral_api_executes_and_preserves_evidence_boundary():
    client = TestClient(
        create_app(
            protocol_registry={"fixture.echo": echo_protocol},
            api_key=API_KEY,
        )
    )

    payload = {
        "protocol_id": "fixture.echo",
        "input_data": {"message": "keyless API MVP"},
        "handoff_id": "SH-HO-API-MVP-001",
        "trace_id": "TRACE-API-MVP-001",
        "evidence_ids": [],
        "boundary_context": {
            "handoff_id": "SH-HO-API-MVP-001",
            "project": "Shirakami API MVP",
            "objective": "Verify provider-neutral HTTP execution",
            "protocol_ids": ["fixture.echo"],
            "evidence_ids": [],
            "verification_scope": ["runtime execution", "evidence", "trace"],
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

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["execution_authorized"] is False
    assert body["publish_authorized"] is False
    assert body["merge_authorized"] is False
    assert body["human_gate_required"] is True
    assert body["trace_id"] == "TRACE-API-MVP-001"
    assert body["evidence_ids"]
    assert body["transition"]["kind"] == "api.mvp.fixture"

    execution_id = body["execution_id"]
    evidence_id = body["evidence_ids"][0]

    execution = client.get(
        f"/v1/executions/{execution_id}",
        headers={"X-API-Key": API_KEY},
    )
    evidence = client.get(
        f"/v1/evidence/{evidence_id}",
        headers={"X-API-Key": API_KEY},
    )
    traceability = client.get(
        "/v1/traceability/TRACE-API-MVP-001",
        headers={"X-API-Key": API_KEY},
    )

    assert execution.status_code == 200
    assert evidence.status_code == 200
    assert traceability.status_code == 200
    assert execution.json()["evidence_ids"] == [evidence_id]
    assert evidence.json()["evidence_id"] == evidence_id
    assert traceability.json()["valid"] is True


def test_keyless_api_requires_authentication():
    client = TestClient(
        create_app(
            protocol_registry={"fixture.echo": echo_protocol},
            api_key=API_KEY,
        )
    )

    response = client.post(
        "/v1/execute",
        json={
            "protocol_id": "fixture.echo",
            "input_data": {"message": "unauthenticated"},
            "handoff_id": "SH-HO-AUTH-001",
            "trace_id": "TRACE-AUTH-001",
            "evidence_ids": [],
            "boundary_context": {
                "handoff_id": "SH-HO-AUTH-001",
                "project": "Shirakami API MVP",
                "objective": "Verify API authentication boundary",
                "protocol_ids": ["fixture.echo"],
                "evidence_ids": [],
                "verification_scope": ["authentication"],
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
                "human_gate_required": True,
            },
        },
    )

    assert response.status_code in (401, 403)

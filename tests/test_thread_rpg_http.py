import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from api.http import create_app
from runtime.adapter import PipelineAdapter


def make_adapter():
    def backend(request):
        return {
            "phase": request.phase,
            "action": request.action,
            "perspective_id": request.input.get("perspective_id"),
            "observed": True,
        }

    return PipelineAdapter(backend=backend, backend_id="http-test-adapter")


def request_body():
    return {
        "task": {"question": "What should we examine?"},
        "perspectives": [
            {"id": "A", "description": "Perspective A"},
            {"id": "B", "description": "Perspective B"},
        ],
        "context": {},
        "protocol_id": "thread_rpg",
        "version": "0.1",
    }


def test_thread_rpg_http_requires_configured_api_key():
    client = TestClient(
        create_app(
            api_key="test-secret",
            thread_rpg_adapter=make_adapter(),
        )
    )

    response = client.post(
        "/v1/thread-rpg/execute",
        json=request_body(),
    )

    assert response.status_code == 401


def test_thread_rpg_http_returns_503_without_adapter():
    client = TestClient(create_app())

    response = client.post(
        "/v1/thread-rpg/execute",
        json=request_body(),
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "ThreadRPG adapter is not configured"


def test_thread_rpg_http_executes_with_adapter_and_api_key():
    client = TestClient(
        create_app(
            api_key="test-secret",
            thread_rpg_adapter=make_adapter(),
        )
    )

    response = client.post(
        "/v1/thread-rpg/execute",
        headers={"X-API-Key": "test-secret"},
        json=request_body(),
    )

    assert response.status_code == 200, response.text
    body = response.json()

    assert body["protocol_id"] == "thread_rpg"
    assert body["perspective_ids"] == ["A", "B"]
    assert len(body["observations"]) == 2
    assert body["conference"] is not None
    assert body["matome"] is not None
    assert body["human_gate_required"] is True
    assert body["decision_authority"] is False
    evidence_ids = body["evidence_ids"]
    assert len(evidence_ids) == 4

    assert all(
        isinstance(evidence_id, str) and evidence_id
        for evidence_id in evidence_ids
    )

    evidence_response = client.get(
        "/v1/evidence",
        headers={"X-API-Key": "test-secret"},
        params={"protocol_id": "thread_rpg"},
    )
    assert evidence_response.status_code == 200
    records = evidence_response.json()

    thread_records = [
        record
        for record in records
        if record["evidence_id"] in evidence_ids
    ]
    assert len(thread_records) == 4

    transition_kinds = {
        record["transition_kind"]
        for record in thread_records
    }
    assert transition_kinds == {
        "thread_rpg.observation:A",
        "thread_rpg.observation:B",
        "thread_rpg.conference",
        "thread_rpg.matome",
    }

    for evidence_id in evidence_ids:
        detail_response = client.get(
            f"/v1/evidence/{evidence_id}",
            headers={"X-API-Key": "test-secret"},
        )
        assert detail_response.status_code == 200
        assert detail_response.json()["evidence_id"] == evidence_id

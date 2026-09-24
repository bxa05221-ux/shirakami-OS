"""API boundary tests for attributable Interpretation identity."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from api.runtime_api import create_app


def _evidence_payload():
    return {
        "protocol_id": "interpretation-api-test",
        "status": "completed",
        "transition_kind": "api.test",
        "transition_data": {"changed": True, "value": "observed"},
        "signals": ["execution.completed"],
    }


def test_interpretation_api_registers_and_retrieves_by_stable_identity():
    client = TestClient(create_app())
    evidence = client.post("/v0.1/evidence", json=_evidence_payload())
    assert evidence.status_code == 201
    evidence_id = evidence.json()["evidence_id"]

    payload = {
        "source_evidence": [evidence_id],
        "actor_id": "ai:researcher",
        "content": {"meaning": "observed transition suggests a state change"},
    }
    created = client.post("/v0.1/interpretations", json=payload)
    assert created.status_code == 201
    body = created.json()
    interpretation_id = body["interpretation_id"]
    assert interpretation_id
    assert body["status"] == "proposed"
    assert body["source_evidence"] == [evidence_id]

    fetched = client.get(f"/v0.1/interpretations/{interpretation_id}")
    assert fetched.status_code == 200
    assert fetched.json() == body


def test_interpretation_api_rejects_missing_source_evidence():
    client = TestClient(create_app())
    response = client.post(
        "/v0.1/interpretations",
        json={
            "source_evidence": ["missing-evidence"],
            "actor_id": "ai:researcher",
            "content": {"meaning": "unfounded"},
        },
    )
    assert response.status_code == 404


def test_interpretation_api_returns_404_for_unknown_identity():
    client = TestClient(create_app())
    response = client.get("/v0.1/interpretations/not-found")
    assert response.status_code == 404

"""API boundary tests for stable Evidence identity."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from api.runtime_api import create_app


def test_evidence_api_registers_and_retrieves_by_stable_identity():
    client = TestClient(create_app())
    payload = {
        "protocol_id": "api-test",
        "status": "completed",
        "transition_kind": "api.test",
        "transition_data": {"changed": True, "value": "ok"},
        "signals": ["execution.completed"],
        "confidence": "observed",
    }

    created = client.post("/v0.1/evidence", json=payload)
    assert created.status_code == 201
    body = created.json()
    evidence_id = body["evidence_id"]
    assert evidence_id
    assert body["protocol_id"] == "api-test"

    fetched = client.get(f"/v0.1/evidence/{evidence_id}")
    assert fetched.status_code == 200
    assert fetched.json() == body


def test_evidence_api_returns_404_for_unknown_identity():
    client = TestClient(create_app())
    response = client.get("/v0.1/evidence/not-found")
    assert response.status_code == 404

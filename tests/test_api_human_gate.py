"""API boundary tests for explicit Human Gate authorization."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient
from api.runtime_api import create_app


def _setup(client):
    evidence = client.post("/v0.1/evidence", json={
        "protocol_id": "human-gate-api-test", "status": "completed",
        "transition_kind": "api.test", "transition_data": {"value": "observed"},
        "signals": ["execution.completed"],
    }).json()
    interpretation = client.post("/v0.1/interpretations", json={
        "source_evidence": [evidence["evidence_id"]], "actor_id": "ai:researcher",
        "content": {"meaning": "proposal"},
    }).json()
    decision = client.post("/v0.1/decisions", json={
        "actor_id": "human:decision-maker", "target": interpretation["interpretation_id"],
        "content": {"action": "accept"}, "timestamp": "2026-09-23T12:00:00+09:00",
    }).json()
    return decision["decision_id"], evidence["evidence_id"]


def test_human_gate_approves_explicit_decision_and_emits_envelope():
    client = TestClient(create_app())
    decision_id, evidence_id = _setup(client)
    response = client.post("/v0.1/human-gate", json={
        "decision_id": decision_id, "reviewer": "human:reviewer",
        "result": "approved", "timestamp": "2026-09-23T12:01:00+09:00",
    })
    assert response.status_code == 201
    body = response.json()
    assert body["decision_id"] == decision_id
    assert body["approval"]["execution_authorized"] is True
    assert body["approval"]["reviewer"] == "human:reviewer"
    assert body["approval"]["evidence_ids"] == [evidence_id]


def test_human_gate_rejects_missing_reviewer():
    client = TestClient(create_app())
    decision_id, _ = _setup(client)
    response = client.post("/v0.1/human-gate", json={
        "decision_id": decision_id, "reviewer": "", "result": "approved",
        "timestamp": "2026-09-23T12:01:00+09:00",
    })
    assert response.status_code == 403


def test_human_gate_requires_existing_decision():
    client = TestClient(create_app())
    response = client.post("/v0.1/human-gate", json={
        "decision_id": "missing", "reviewer": "human:reviewer", "result": "approved",
        "timestamp": "2026-09-23T12:01:00+09:00",
    })
    assert response.status_code == 404

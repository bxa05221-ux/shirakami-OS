"""API boundary tests for explicit human Decision authority."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from api.runtime_api import create_app


def _setup(client):
    evidence = client.post("/v0.1/evidence", json={
        "protocol_id": "decision-api-test",
        "status": "completed",
        "transition_kind": "api.test",
        "transition_data": {"value": "observed"},
        "signals": ["execution.completed"],
    }).json()
    interpretation = client.post("/v0.1/interpretations", json={
        "source_evidence": [evidence["evidence_id"]],
        "actor_id": "ai:researcher",
        "content": {"meaning": "proposal"},
    }).json()
    return interpretation["interpretation_id"]


def test_decision_api_requires_explicit_human_actor_and_preserves_identity():
    client = TestClient(create_app())
    target = _setup(client)
    payload = {
        "actor_id": "human:reviewer",
        "target": target,
        "content": {"action": "accepted"},
        "timestamp": "2026-09-23T12:00:00+09:00",
    }
    created = client.post("/v0.1/decisions", json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["decision_id"]
    assert body["actor_id"] == "human:reviewer"
    assert body["target"] == target

    fetched = client.get(f"/v0.1/decisions/{body['decision_id']}")
    assert fetched.status_code == 200
    assert fetched.json() == body


def test_decision_api_rejects_non_human_authority_labels():
    client = TestClient(create_app())
    target = _setup(client)
    response = client.post("/v0.1/decisions", json={
        "actor_id": "ai",
        "target": target,
        "content": {"action": "accepted"},
        "timestamp": "2026-09-23T12:00:00+09:00",
    })
    assert response.status_code == 403


def test_decision_api_requires_existing_interpretation():
    client = TestClient(create_app())
    response = client.post("/v0.1/decisions", json={
        "actor_id": "human:reviewer",
        "target": "missing-interpretation",
        "content": {"action": "accepted"},
        "timestamp": "2026-09-23T12:00:00+09:00",
    })
    assert response.status_code == 404


def test_decision_lineage_requires_existing_superseded_decision():
    client = TestClient(create_app())
    target = _setup(client)
    response = client.post("/v0.1/decisions", json={
        "actor_id": "human:reviewer",
        "target": target,
        "content": {"action": "revised"},
        "timestamp": "2026-09-23T12:00:00+09:00",
        "supersedes": "missing-decision",
    })
    assert response.status_code == 404

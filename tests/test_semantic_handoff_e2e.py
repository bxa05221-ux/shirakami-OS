"""End-to-end contract test for the public SemanticHandoff HTTP boundary."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from shbb_api.app import create_app


def test_handoff_round_trip_preserves_lineage_and_has_no_authority_inference():
    client = TestClient(create_app())
    payload = {
        "evidence_ids": ["e-001", "e-002"],
        "interpretation_id": "i-001",
        "decision_id": "d-001",
        "gate_id": "g-001",
        "payload": {"renderer": "json", "purpose": "external-consumer", "value": {"x": 1}},
    }

    response = client.post("/handoff", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["evidence_ids"] == payload["evidence_ids"]
    assert body["interpretation_id"] == payload["interpretation_id"]
    assert body["decision_id"] == payload["decision_id"]
    assert body["gate_id"] == payload["gate_id"]
    assert body["payload"] == payload["payload"]
    assert body["authority"] == "not_inferred"
    assert isinstance(body["handoff_id"], str)
    assert len(body["handoff_id"]) == 64

    repeat = client.post("/handoff", json=payload)
    assert repeat.status_code == 200
    assert repeat.json() == body


def test_handoff_is_transport_only_when_authority_like_payload_is_present():
    client = TestClient(create_app())
    response = client.post("/handoff", json={
        "evidence_ids": ["e-001"],
        "payload": {"approval": True, "authorized_by": "ai"},
    })
    assert response.status_code == 200
    assert response.json()["authority"] == "not_inferred"
    assert response.json()["payload"]["approval"] is True

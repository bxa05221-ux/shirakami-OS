"""Public HTTP boundary tests for SemanticHandoff."""

from pathlib import Path
import sys

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shbb-api"))

from fastapi.testclient import TestClient

from app import create_app


def test_handoff_round_trip_is_stable_and_non_authoritative():
    client = TestClient(create_app())
    payload = {
        "evidence_ids": ["e-001"],
        "interpretation_id": "i-001",
        "decision_id": "d-001",
        "gate_id": "g-001",
        "payload": {"renderer": "json", "purpose": "external-consumer"},
    }
    first = client.post("/handoff", json=payload)
    second = client.post("/handoff", json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert first.json()["authority"] == "not_inferred"


def test_handoff_rejects_invalid_evidence_ids():
    client = TestClient(create_app())
    response = client.post("/handoff", json={"evidence_ids": [""]})
    assert response.status_code == 400


def test_observe_still_rejects_authority_fields():
    client = TestClient(create_app())
    response = client.post("/observe", json={
        "landscape_id": "test",
        "input": {},
        "approval": True,
    })
    assert response.status_code == 400

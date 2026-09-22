"""Phase 2 API authority-boundary invariants."""

from pathlib import Path
import sys

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shbb-api"))

from app import create_app


def test_observe_does_not_create_authority_fields():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe",
        json={
            "landscape_id": "example",
            "input": {"text": "x"},
            "protocol_id": "protocol.example.v1",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["protocol_id"] == "protocol.example.v1"
    assert "approval" not in body
    assert "approval_envelope" not in body
    assert "execution_authorized" not in body
    assert "human_authorized" not in body


def test_observe_is_not_an_execution_endpoint():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe",
        json={
            "landscape_id": "example",
            "input": {"protocol": "candidate"},
            "protocol_id": "candidate.protocol.v1",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["state"] == "observed"
    assert body["provenance"]["transition"] is False
    assert "execution_id" not in body
    assert "transition" not in body["result"]

"""API semantic handoff boundary verification."""

from pathlib import Path
import sys

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shbb-api"))

from app import create_app


def test_observe_rejects_authority_fields():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe",
        json={
            "landscape_id": "example",
            "input": {"text": "x"},
            "protocol_id": "protocol.example.v1",
            "execution_authorized": True,
        },
    )

    assert response.status_code == 400
    assert "authority fields" in response.json()["detail"]


def test_observe_does_not_infer_protocol_identity():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe",
        json={"landscape_id": "example", "input": {"text": "x"}},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["protocol_id"] is None
    assert body["provenance"]["transition"] is False
    assert "execution_id" not in body

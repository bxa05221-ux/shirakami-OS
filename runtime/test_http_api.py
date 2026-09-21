"""Tests for the HTTP transport boundary alpha 0.1."""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from api.http import create_app
from runtime.api import ShirakamiAPI
from runtime.evolution_pipeline import EvidenceDrivenRuntime
from runtime.prototype import Transition


def _protocol(_: Any) -> Transition:
    return Transition(kind="http.example", data={"changed": True})


def _client() -> TestClient:
    return TestClient(
        create_app(
            ShirakamiAPI(EvidenceDrivenRuntime()),
            {"http.example": _protocol},
        )
    )


def _context() -> dict[str, Any]:
    return {
        "protocol_id": "http.example",
        "landscape": {"topic": "ui-for-ai"},
        "metadata": {"source": "http-test"},
    }


def test_health() -> None:
    response = _client().get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_observe_and_evidence_are_json_transport() -> None:
    client = _client()
    response = client.post(
        "/v1/observe",
        json={"observation": {"signal": "hello"}, "context": _context()},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["state"] == "EVIDENCE"
    assert any(
        item["signals"] == ["CONTEXT_SNAPSHOT"]
        for item in body["evidence"]
    )

    evidence = client.get(
        "/v1/evidence",
        params={"signal": "CONTEXT_SNAPSHOT"},
    )
    assert evidence.status_code == 200
    assert evidence.json()


def test_approval_cannot_be_inferred_over_http() -> None:
    client = _client()
    client.post(
        "/v1/observe",
        json={"observation": {}, "context": _context()},
    )
    client.post(
        "/v1/analyze",
        json={
            "protocol_id": "http.new",
            "protocol_exists": False,
            "diff_ref": "diff-http-1",
        },
    )

    denied = client.post(
        "/v1/approve",
        json={"approved": True, "reviewer": "human"},
    )
    assert denied.status_code == 200
    assert denied.json()["accepted"] is False

    approved = client.post(
        "/v1/approve",
        json={
            "approved": True,
            "reviewer": "human",
            "human_authorized": True,
        },
    )
    assert approved.status_code == 200
    assert approved.json()["accepted"] is True


def test_execute_requires_registered_protocol() -> None:
    client = _client()
    missing = client.post(
        "/v1/execute",
        json={"protocol_id": "unknown", "input_data": {}},
    )
    assert missing.status_code == 404

    client.post(
        "/v1/observe",
        json={"observation": {}, "context": _context()},
    )
    client.post(
        "/v1/analyze",
        json={"protocol_id": "http.example", "protocol_exists": True},
    )
    executed = client.post(
        "/v1/execute",
        json={"protocol_id": "http.example", "input_data": {"x": 1}},
    )
    assert executed.status_code == 200
    assert executed.json()["status"] == "completed"

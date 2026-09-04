"""External-facing E2E contract tests for the alpha API.

These tests use FastAPI's TestClient when the optional HTTP dependency is
installed. They verify HTTP boundaries without performing a real GitHub write.
"""

import pytest

fastapi = pytest.importorskip("fastapi")
httpx = pytest.importorskip("httpx")

from api.runtime_api import create_app


def test_http_execute_e2e():
    from fastapi.testclient import TestClient

    client = TestClient(create_app())

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok", "version": "0.1.0"}

    response = client.post(
        "/v0.1/execute",
        json={
            "protocol": {"matome": {"title": "External E2E", "version": "0.1"}},
            "operation": "echo",
            "input": {"landscape": "external-test"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["protocol"]["title"] == "External E2E"
    assert body["success"] is True
    assert body["event"] == "execution.completed"
    assert body["output"] == {"landscape": "external-test"}


def test_http_oppai_normalize_e2e():
    from fastapi.testclient import TestClient

    client = TestClient(create_app())
    response = client.post(
        "/v0.1/oppai/normalize",
        json={"text": "いや、そこは違う。どうして？"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["schema"] == "OPPAI"
    assert body["version"] == "0.1"
    assert body["event"] == "oppai.observed"
    assert body["raw_input"] == "いや、そこは違う。どうして？"
    assert body["canonical_prompt"] == body["raw_input"]
    assert body["corrections"] == ["いや、そこは違う。"]
    assert body["unresolved"] == ["どうして？"]
    assert body["interaction_signals"] == []
    assert body["confidence"] == "provisional"

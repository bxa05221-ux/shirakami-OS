"""External-facing E2E contract test for the alpha API.

This test uses FastAPI's TestClient when the optional HTTP dependency is
installed. It verifies the HTTP boundary without performing a real GitHub
write.
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

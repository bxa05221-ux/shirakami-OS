"""R0064 operational check for the existing Runtime HTTP execution boundary."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from api.runtime_api import create_app


def test_r0064_runtime_api_executes_existing_protocol_boundary():
    client = TestClient(create_app())

    response = client.post(
        "/v0.1/execute",
        json={
            "protocol": {"matome": {"title": "R0064 operation", "version": "0.1"}},
            "operation": "echo",
            "input": {"operation": "r0064", "continuity": "observed"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["protocol"] == {"title": "R0064 operation", "version": "0.1"}
    assert body["success"] is True
    assert body["event"] == "execution.completed"
    assert body["output"] == {"operation": "r0064", "continuity": "observed"}
    assert body["error"] is None

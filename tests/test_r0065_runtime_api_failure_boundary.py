"""R0065 operational check for the Runtime API failure boundary."""

import pytest

fastapi = pytest.importorskip("fastapi")
httpx = pytest.importorskip("httpx")

from api.runtime_api import create_app


def test_runtime_api_failed_execution_does_not_report_success():
    from fastapi.testclient import TestClient

    client = TestClient(create_app())
    response = client.post(
        "/v0.1/execute",
        json={
            "protocol": {"matome": {"title": "R0065 Failure", "version": "0.1"}},
            "operation": "unsupported-operation",
            "input": {"landscape": "failure-boundary"},
        },
    )

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["event"] == "execution.failed"
    assert body["output"] is None
    assert body["error"]

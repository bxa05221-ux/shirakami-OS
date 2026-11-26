"""Regression tests for the fail-closed third-party evaluation HTTP boundary."""

import pytest
from fastapi.testclient import TestClient

from api.http import create_app


def test_evaluation_mode_rejects_sync_adapter():
    with pytest.raises(ValueError, match="forbids arbitrary model adapters"):
        create_app(evaluation_mode=True, model_adapter=lambda prompt, protocol: "external")


def test_evaluation_mode_rejects_async_adapter():
    async def adapter(prompt, protocol):
        return "external"

    with pytest.raises(ValueError, match="forbids arbitrary model adapters"):
        create_app(evaluation_mode=True, async_model_adapter=adapter)


def test_evaluation_execute_is_denied_before_runtime_or_adapter():
    client = TestClient(create_app(api_key="fixture-key", evaluation_mode=True))
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "fixture-key"},
        json={
            "protocol_id": "fixture",
            "input_data": {"observation": "confidential"},
            "handoff_id": "fixture-handoff",
            "evidence_ids": [],
            "boundary_context": {
                "handoff_id": "fixture-handoff",
                "project": "evaluation-fixture",
                "objective": "must not execute",
                "protocol_ids": ["fixture"],
                "evidence_ids": [],
            },
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == (
        "evaluation execution disabled until audited local runtime is available"
    )


def test_evaluation_execute_stays_closed_after_late_async_adapter_injection():
    """Synthetic-only: late adapter mutation must not reach the external callback."""
    from api.http import ShirakamiHTTPTransport

    calls = []

    async def forbidden_adapter(prompt, protocol):
        calls.append((prompt, protocol))
        raise AssertionError("evaluation data reached arbitrary async adapter")

    transport = ShirakamiHTTPTransport(api_key="fixture-key", evaluation_mode=True)
    transport.async_model_adapter = forbidden_adapter
    client = TestClient(transport.create_app())
    response = client.post(
        "/v1/execute",
        headers={"X-API-Key": "fixture-key"},
        json={
            "protocol_id": "fixture",
            "input_data": {"observation": "synthetic-confidential"},
            "handoff_id": "fixture-handoff",
            "evidence_ids": [],
            "boundary_context": {
                "handoff_id": "fixture-handoff",
                "project": "evaluation-fixture",
                "objective": "must not execute",
                "protocol_ids": ["fixture"],
                "evidence_ids": [],
            },
        },
    )
    assert response.status_code == 403
    assert calls == []


def test_general_mode_retains_adapter_registration():
    adapter = lambda prompt, protocol: "fixture"
    app = create_app(model_adapter=adapter)
    assert app is not None

@pytest.mark.parametrize("method,path", [
    ("POST", "/v1/reviews/register"),
    ("POST", "/v1/reviews/submit"),
    ("POST", "/v1/reviews/blind"),
    ("POST", "/v1/reviews/blind/comparative/aiwitness"),
    ("POST", "/v1/reviews/comparative"),
    ("POST", "/v1/reviews/comparative/aiwitness"),
    ("GET", "/v1/reviews/comparative/project-a"),
    ("GET", "/v1/reviews/project-a"),
])
def test_evaluation_reviewer_routes_fail_closed_without_verified_membership(method, path):
    client = TestClient(create_app(api_key="fixture-key", evaluation_mode=True))
    response = client.request(method, path, headers={"X-API-Key": "fixture-key"}, json={} if method == "POST" else None)
    assert response.status_code == 403
    assert response.json()["detail"] == (
        "evaluation reviewer routes disabled until authenticated project membership is enforced"
    )

@pytest.mark.parametrize("method,path", [
    ("GET", "/v1/capabilities"),
    ("POST", "/v1/observe"),
    ("POST", "/v1/analyze"),
    ("POST", "/v1/approve"),
    ("GET", "/v1/executions/fixture"),
    ("GET", "/v1/traces/fixture"),
    ("GET", "/v1/witnesses/fixture/history"),
    ("GET", "/v1/witnesses/fixture"),
    ("GET", "/v1/traceability/fixture"),
    ("POST", "/v1/executions/fixture/verify"),
    ("GET", "/v1/evidence"),
    ("GET", "/v1/evidence/fixture"),
])
def test_evaluation_other_routes_fail_closed(method, path):
    client = TestClient(create_app(api_key="fixture-key", evaluation_mode=True))
    response = client.request(method, path, headers={"X-API-Key": "fixture-key"}, json={} if method == "POST" else None)
    assert response.status_code == 403
    assert response.json()["detail"] == "evaluation API disabled until authenticated local runtime is available"


def test_evaluation_health_stays_available():
    client = TestClient(create_app(api_key="fixture-key", evaluation_mode=True))
    assert client.get("/health").status_code == 200

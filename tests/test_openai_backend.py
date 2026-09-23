"""Deterministic contract tests for the external OpenAI backend adapter."""

import json

from runtime.openai_backend import OpenAIBackend


def test_openai_backend_translates_handoff_and_preserves_request_id():
    captured = {}

    def fake_transport(request):
        captured["url"] = request.full_url
        captured["authorization"] = request.get_header("Authorization")
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return json.dumps({"id": "resp-test-001", "output": []}).encode("utf-8")

    backend = OpenAIBackend(
        api_key="test-key",
        model="test-model",
        endpoint="https://example.test/v1/responses",
        transport=fake_transport,
    )
    response = backend.execute(
        {"request_id": "req-001", "input": "hello"}
    )

    assert response.backend_id == "openai-responses:v0.1"
    assert response.status == "completed"
    assert captured["url"] == "https://example.test/v1/responses"
    assert captured["authorization"] == "Bearer test-key"
    assert captured["body"] == {"model": "test-model", "input": "hello"}
    assert response.payload["id"] == "resp-test-001"
    assert response.payload["request_id"] == "req-001"
    assert "authority" not in response.payload


def test_openai_backend_requires_api_key():
    try:
        OpenAIBackend(api_key="")
    except ValueError as exc:
        assert str(exc) == "api_key is required"
    else:
        raise AssertionError("missing API key must be rejected")

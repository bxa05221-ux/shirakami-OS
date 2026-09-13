import json

from runtime.real_model_adapter import ModelRequest
from experiments.openai_responses_transport import openai_responses_transport


class _FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps({"output": "observed"}).encode("utf-8")


def test_openai_transport_builds_provider_request_without_exposing_credentials(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-secret")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    observed = {}

    def fake_urlopen(request, timeout):
        observed["request"] = request
        observed["timeout"] = timeout
        return _FakeResponse()

    monkeypatch.setattr("experiments.openai_responses_transport.urlopen", fake_urlopen)

    result = openai_responses_transport(
        ModelRequest(
            canonical_prompt="canonical input",
            context={"protocol_id": "test.protocol"},
        )
    )

    request = observed["request"]
    payload = json.loads(request.data.decode("utf-8"))

    assert result == {"output": "observed"}
    assert payload == {"model": "test-model", "input": "canonical input"}
    assert request.get_header("Authorization") == "Bearer test-secret"
    assert request.get_header("Content-type") == "application/json"
    assert observed["timeout"] == 60

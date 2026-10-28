"""Contract tests for the UMR HTTP backend."""

import json
from urllib.error import URLError

import pytest

from runtime.umr_backend import UMRBackend, UMRBackendError


def fake_transport_for(result, captured):
    def transport(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["timeout"] = timeout
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return json.dumps(result).encode("utf-8")
    return transport


def test_umr_backend_sends_task_and_admitted_context_only():
    captured = {}
    backend = UMRBackend(
        transport=fake_transport_for(
            {
                "status": "success",
                "engine": "mock",
                "output": {"text": "test result"},
                "error": None,
            },
            captured,
        )
    )

    response = backend.execute(
        {
            "request_id": "req-001",
            "input": {"question": "hello"},
            "context_bundle": {
                "request_id": "req-001",
                "evidence": [{"evidence_id": "e-001", "value": "selected"}],
            },
            "context_lineage": {"evidence_ids": ["e-001"]},
            "evidence_store": {
                "e-001": {"value": "selected"},
                "e-secret": {"value": "must-not-be-sent"},
            },
            "authority": "not_inferred",
        }
    )

    assert captured["url"] == "http://127.0.0.1:8766/v1/execute"
    assert captured["method"] == "POST"
    assert captured["timeout"] == 30.0
    assert captured["body"]["engine"] == "mock"

    sent_text = captured["body"]["input"]["text"]
    sent_document = json.loads(sent_text)
    assert sent_document["task_input"] == {"question": "hello"}
    assert sent_document["context_bundle"]["evidence"][0]["evidence_id"] == "e-001"
    assert "e-secret" not in sent_text
    assert "context_lineage" not in sent_text
    assert "authority" not in sent_text

    assert response.backend_id == "universal-model-runtime:v0.1"
    assert response.status == "completed"
    assert response.payload["output"] == {"text": "test result"}
    assert response.payload["request_id"] == "req-001"
    assert "authority" not in response.payload


def test_umr_backend_accepts_payload_as_task_input():
    captured = {}
    backend = UMRBackend(
        transport=fake_transport_for(
            {"status": "success", "engine": "mock", "output": {"text": "ok"}},
            captured,
        )
    )

    backend.execute({"payload": {"task": "summarize"}})

    sent = json.loads(captured["body"]["input"]["text"])
    assert sent == {"task_input": {"task": "summarize"}}


@pytest.mark.parametrize(
    "result",
    [
        [],
        {"status": "error", "engine": "mock", "output": {}},
        {"status": "success", "engine": "other", "output": {}},
        {"status": "success", "engine": "mock", "output": None},
    ],
)
def test_umr_backend_rejects_invalid_responses(result):
    backend = UMRBackend(transport=fake_transport_for(result, {}))

    with pytest.raises(UMRBackendError):
        backend.execute({"input": "hello"})


def test_umr_backend_rejects_invalid_json():
    backend = UMRBackend(transport=lambda request, timeout: b"not-json")

    with pytest.raises(UMRBackendError, match="invalid JSON"):
        backend.execute({"input": "hello"})


def test_umr_backend_wraps_transport_failure():
    def failing_transport(request, timeout):
        raise URLError("offline")

    backend = UMRBackend(transport=failing_transport)

    with pytest.raises(UMRBackendError, match="request failed"):
        backend.execute({"input": "hello"})


def test_umr_backend_requires_task_input():
    backend = UMRBackend(transport=lambda request, timeout: b"{}")

    with pytest.raises(ValueError, match="input or payload"):
        backend.execute({"request_id": "req-001"})


def test_umr_backend_validates_configuration():
    with pytest.raises(ValueError, match="base_url"):
        UMRBackend(base_url="")

    with pytest.raises(ValueError, match="engine"):
        UMRBackend(engine=" ")

    with pytest.raises(ValueError, match="timeout"):
        UMRBackend(timeout=0)

"""HTTP contract tests for the shbb-api observation boundary."""

from pathlib import Path
import sys

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

# Keep the external API artifact directory name as ``shbb-api`` while making
# its Python module importable for the test runner.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shbb-api"))

from app import ObserveResponse, create_app


def test_observe_e2e():
    from fastapi.testclient import TestClient

    client = TestClient(create_app())
    response = client.post(
        "/observe",
        json={
            "landscape_id": "example-landscape",
            "input": {"text": "今日は少し疲れた"},
        },
    )

    assert response.status_code == 200
    body = response.json()
    validated = ObserveResponse.model_validate(body)
    assert validated.landscape_id == "example-landscape"
    assert validated.state == "observed"
    assert validated.result == {"text": "今日は少し疲れた"}
    assert validated.evidence_id is None
    assert validated.protocol_id is None
    assert validated.provenance.transition is False
    assert len(validated.observation_id) == 16


def test_observe_preserves_explicit_protocol_reference():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe",
        json={
            "landscape_id": "example",
            "input": {"text": "x"},
            "protocol_id": "protocol.example.v1",
        },
    )

    assert response.status_code == 200
    assert response.json()["protocol_id"] == "protocol.example.v1"


def test_observe_accepts_client_metadata_without_treating_it_as_result():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe",
        json={
            "landscape_id": "example",
            "input": {"text": "x"},
            "metadata": {"trace": "client-only"},
        },
    )

    assert response.status_code == 200
    assert response.json()["result"] == {"text": "x"}
    assert "metadata" not in response.json()["result"]


def test_observe_rejects_missing_landscape_id():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe", json={"input": {"text": "x"}}
    )
    assert response.status_code == 400


def test_observe_rejects_empty_landscape_id():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe", json={"landscape_id": "", "input": {"text": "x"}}
    )
    assert response.status_code == 400


def test_observe_rejects_non_object_input():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe", json={"landscape_id": "example", "input": "x"}
    )
    assert response.status_code == 400


@pytest.mark.parametrize("body", [["invalid"], "invalid"])
def test_observe_rejects_non_object_request_body(body):
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post("/observe", json=body)
    assert response.status_code == 400


def test_observe_rejects_malformed_json_request_body():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe",
        content=b'{"landscape_id":"example","input":{"text":"x"}',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400


def test_observe_response_schema_rejects_invalid_state():
    from pydantic import ValidationError

    payload = {
        "landscape_id": "example",
        "observation_id": "0123456789abcdef",
        "state": "changed",
        "evidence_id": None,
        "protocol_id": None,
        "result": {},
        "provenance": {"runtime": "test", "transition": False},
    }

    with pytest.raises(ValidationError):
        ObserveResponse.model_validate(payload)


def test_observe_response_schema_rejects_invalid_observation_id():
    from pydantic import ValidationError

    payload = {
        "landscape_id": "example",
        "observation_id": "not-a-valid-id",
        "state": "observed",
        "evidence_id": None,
        "protocol_id": None,
        "result": {},
        "provenance": {"runtime": "test", "transition": False},
    }

    with pytest.raises(ValidationError):
        ObserveResponse.model_validate(payload)

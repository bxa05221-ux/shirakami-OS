"""HTTP contract tests for the shbb-api observation boundary."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from shbb_api.app import create_app


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
    assert body["landscape_id"] == "example-landscape"
    assert body["state"] == "observed"
    assert body["result"] == {"text": "今日は少し疲れた"}
    assert body["evidence_id"] is None
    assert body["provenance"]["transition"] is False
    assert len(body["observation_id"]) == 16


def test_observe_rejects_missing_landscape_id():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe", json={"input": {"text": "x"}}
    )
    assert response.status_code == 400


def test_observe_rejects_non_object_input():
    from fastapi.testclient import TestClient

    response = TestClient(create_app()).post(
        "/observe", json={"landscape_id": "example", "input": "x"}
    )
    assert response.status_code == 400

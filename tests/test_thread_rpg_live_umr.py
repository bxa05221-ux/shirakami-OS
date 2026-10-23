import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from api.http import create_app
from runtime.thread_rpg_umr_adapter import create_thread_rpg_umr_adapter


def test_thread_rpg_http_uses_live_umr_mock_server():
    adapter = create_thread_rpg_umr_adapter(
        base_url="http://127.0.0.1:8766",
        engine="mock",
        timeout=30.0,
    )

    client = TestClient(
        create_app(
            api_key="test-secret",
            thread_rpg_adapter=adapter,
        )
    )

    response = client.post(
        "/v1/thread-rpg/execute",
        headers={"X-API-Key": "test-secret"},
        json={
            "task": {"question": "Explore different interpretations"},
            "perspectives": [
                {"id": "A", "description": "Character motives"},
                {"id": "B", "description": "Social context"},
            ],
            "context": {"source": "live-umr-test"},
            "protocol_id": "thread_rpg",
            "version": "0.1",
        },
    )

    assert response.status_code == 200, response.text
    body = response.json()

    assert body["perspective_ids"] == ["A", "B"]
    assert len(body["observations"]) == 2
    assert body["conference"] is not None
    assert body["matome"] is not None
    assert body["human_gate_required"] is True
    assert body["decision_authority"] is False

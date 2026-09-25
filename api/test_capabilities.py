from fastapi.testclient import TestClient

from api.http import create_app


API_KEY = "test-shirakami-key"


def test_capabilities_requires_api_key() -> None:
    client = TestClient(create_app(api_key=API_KEY))
    response = client.get("/v1/capabilities")
    assert response.status_code == 401


def test_capabilities_reports_current_non_authoritative_boundary() -> None:
    client = TestClient(create_app(api_key=API_KEY))
    response = client.get("/v1/capabilities", headers={"X-API-Key": API_KEY})

    assert response.status_code == 200
    body = response.json()

    assert body["api"] == {
        "name": "Shirakami UI for AI API",
        "version": "alpha-0.1",
    }
    assert all(body["supports"].values())
    assert body["boundaries"] == {
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
        "decision_authority": False,
    }
    assert body["reviewer"] == {
        "matome_yaml": "context_only",
        "comparative_decision": None,
        "reviewer_perspectives_preserved": True,
    }

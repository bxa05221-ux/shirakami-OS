from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_execute_v1():
    response = client.post(
        "/v1/execute",
        json={
            "protocol": {"matome": {"title": "HTTP Test", "version": "0.1"}},
            "operation": "echo",
            "input": {"landscape": "test"},
        },
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["output"] == {"landscape": "test"}


def test_observe_does_not_transition_state():
    response = client.post("/v1/observe", json={"observation": {"fact": "observed"}})
    assert response.status_code == 200
    assert response.json()["state_transition"] is False


def test_evidence_lookup_boundary():
    response = client.get("/v1/evidence/example-001")
    assert response.status_code == 200
    assert response.json()["evidence_id"] == "example-001"

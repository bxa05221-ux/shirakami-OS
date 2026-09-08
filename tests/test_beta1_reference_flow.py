from fastapi.testclient import TestClient

from api.runtime_api import create_app


def test_beta1_reference_flow_round_trip():
    client = TestClient(create_app())

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["version"] == "1.0.0"

    protocol = {"matome": {"title": "demo.landscape.message", "version": "0.1"}}
    executed = client.post(
        "/v1/execute",
        json={"protocol": protocol, "operation": "message", "input": {"message": "hello landscape"}},
    )

    assert executed.status_code == 200
    body = executed.json()
    assert body["status"] == "completed"
    assert body["transition"]["kind"] == "landscape.message.received"
    assert body["landscape"]["message"] == "hello landscape"
    assert body["evidence"]["transition_data"]["message"] == "hello landscape"

    landscape = client.post("/v1/landscape/observe")
    assert landscape.status_code == 200
    assert landscape.json()["landscape"]["message"] == "hello landscape"

    evidence = client.post("/v1/evidence/observe")
    assert evidence.status_code == 200
    assert evidence.json()["evidence"][-1]["transition"] == "landscape.message.received"


def test_beta1_adapter_invoke_is_not_implicitly_backend_specific():
    client = TestClient(create_app())
    response = client.post("/v1/adapter/invoke", json={"adapter": "github"})
    assert response.status_code == 501

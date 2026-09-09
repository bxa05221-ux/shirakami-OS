from fastapi.testclient import TestClient

from api.runtime_api import create_app


def test_r0072_runtime_health_boundary_is_observable_without_state_mutation():
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}

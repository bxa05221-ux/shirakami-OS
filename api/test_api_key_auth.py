from fastapi.testclient import TestClient

from api.http import create_app


API_KEY = "test-shirakami-key"


def test_missing_api_key_is_rejected() -> None:
    client = TestClient(create_app(api_key=API_KEY))
    response = client.get("/v1/evidence")
    assert response.status_code == 401


def test_invalid_api_key_is_rejected() -> None:
    client = TestClient(create_app(api_key=API_KEY))
    response = client.get("/v1/evidence", headers={"X-API-Key": "wrong"})
    assert response.status_code == 401


def test_valid_api_key_reaches_runtime() -> None:
    client = TestClient(create_app(api_key=API_KEY))
    response = client.get("/v1/evidence", headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_health_remains_public() -> None:
    client = TestClient(create_app(api_key=API_KEY))
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

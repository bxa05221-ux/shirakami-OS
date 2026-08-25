from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)
FIXTURE = Path(__file__).parent / "fixtures" / "shirakami-model-v3.2.yaml"


def test_v32_fixture_is_real_matome_yaml():
    data = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
    root = data["matome_yaml"]
    assert root["metadata"]["title"] == "白神モデル v3.2"
    assert root["metadata"]["type"] == "的目YAML"
    assert root["metadata"]["status"] == "conceptual_architecture"
    assert root["subject"]["central_concept"][:3] == [
        "Landscape First",
        "Protocol First",
        "Human Context First",
    ]


def test_v32_execute_preserves_protocol_identity_and_input():
    data = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
    root = data["matome_yaml"]
    input_value = {
        "kind": "protocol_fixture",
        "metadata": root["metadata"],
        "core_loop": root["core_loop"],
    }

    response = client.post(
        "/v1/execute",
        json={
            "protocol": {
                "title": root["metadata"]["title"],
                "version": "3.2",
            },
            "input": input_value,
            "context": {"source": "shirakami-model"},
        },
    )

    assert response.status_code == 200
    result = response.json()
    assert result["protocol"]["title"] == "白神モデル v3.2"
    assert result["protocol"]["version"] == "3.2"
    assert result["success"] is True
    assert result["event"] == "execution.completed"
    assert result["output"] == input_value

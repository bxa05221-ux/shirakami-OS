from fastapi.testclient import TestClient

from api.runtime_api import create_app
from runtime.landscape import LandscapeState
from runtime.observable_execution import execute_observably
from runtime.prototype import Runtime, example_protocol


def test_api_execution_and_landscape_observation_remain_independently_consistent():
    client = TestClient(create_app())
    payload = {
        "protocol": {"title": "Example Protocol", "version": "0.1"},
        "operation": "echo",
        "input": {"value": "r0067"},
    }

    response = client.post("/v0.1/execute", json=payload)
    assert response.status_code == 200
    api_result = response.json()

    state = LandscapeState.from_snapshot(
        {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}
    )
    observable = execute_observably(
        state,
        Runtime(),
        "example.protocol",
        example_protocol,
        {"value": "r0067"},
    )

    assert api_result["success"] is True
    assert api_result["protocol"]["version"] == "0.1"
    assert api_result["output"] == {"value": "r0067"}
    assert observable.evidence.protocol_id == "example.protocol"
    assert observable.after_state["input"] == {"value": "r0067"}
    assert observable.observation["snapshot"]["repository"] == "bxa05221-ux/shirakami-OS"
    assert len(observable.observation["evidence_lineage"]) == 1
    assert observable.observation["evidence_lineage"][0]["protocol_id"] == "example.protocol"

    # Correlate only the independently supplied input; do not treat API output
    # as Evidence or semantic authority for the Landscape.
    assert api_result["output"] == observable.after_state["input"]

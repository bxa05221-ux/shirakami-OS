import pytest
from fastapi.testclient import TestClient

from api.http import create_app
from runtime.adapter import PipelineAdapter
from runtime.api import ShirakamiAPI
from runtime.prototype import Transition


HEADERS = {"X-API-Key": "test-secret"}


def request_body():
    return {
        "task": {"question": "What should we examine?"},
        "perspectives": [{"id": "A"}, {"id": "B"}],
        "context": {}, "protocol_id": "thread_rpg", "version": "0.1",
    }


def make_adapter():
    return PipelineAdapter(
        lambda request: {"phase": request.phase, "text": "generated interpretation"},
        backend_id="http-test-adapter",
    )


def test_thread_rpg_http_requires_configured_api_key():
    calls = []
    adapter = PipelineAdapter(lambda request: calls.append(request))
    client = TestClient(create_app(api_key="test-secret", thread_rpg_adapter=adapter))
    response = client.post("/v1/thread-rpg/execute", json=request_body())
    assert response.status_code == 401
    assert calls == []


def test_thread_rpg_http_returns_503_without_adapter():
    client = TestClient(create_app())
    response = client.post("/v1/thread-rpg/execute", json=request_body())
    assert response.status_code == 503


def test_generation_preserves_existing_evidence_trace_witness_and_approval_state():
    api = ShirakamiAPI()
    calls = []

    async def provider(prompt, protocol_id):
        calls.append((prompt, protocol_id))
        return {"text": "fixture model output"}

    def protocol(context):
        return Transition(kind="fixture.transition", data={"output": dict(context.input)})

    # Preserve main's fifth positional argument for the async adapter.
    client = TestClient(create_app(
        api, {"fixture": protocol}, "test-secret", None, provider,
        thread_rpg_adapter=make_adapter(),
    ))
    assert client.post("/v1/observe", headers=HEADERS, json={
        "observation": {}, "context": {"protocol_id": "fixture"}, "handoff_id": "H1",
    }).status_code == 200
    assert client.post("/v1/analyze", headers=HEADERS, json={
        "protocol_id": "fixture", "protocol_exists": False,
    }).status_code == 200
    payload = {
        "protocol_id": "fixture", "input_data": {"text": "prompt"},
        "handoff_id": "H1", "trace_id": "T1", "evidence_ids": [],
        "boundary_context": {
            "handoff_id": "H1", "project": "test", "objective": "regression",
            "protocol_ids": ["fixture"], "evidence_ids": [],
        },
    }
    assert client.post("/v1/execute", headers=HEADERS, json=payload).status_code == 409
    assert calls == []
    assert client.post("/v1/approve", headers=HEADERS, json={
        "approved": True, "human_authorized": True,
    }).json()["accepted"] is True
    executed = client.post("/v1/execute", headers=HEADERS, json=payload)
    assert executed.status_code == 200, executed.text
    assert calls == [("prompt", "fixture")]
    existing = executed.json()
    assert client.post(
        f"/v1/executions/{existing['execution_id']}/verify", headers=HEADERS,
        json={"expected_transition_kind": "fixture.transition"},
    ).json()["status"] == "pass"

    store_before = api.runtime.store
    state_before = api.runtime.loop.state
    trace_before = client.get("/v1/traces/T1", headers=HEADERS).json()
    witness_before = client.get("/v1/witnesses/T1/history", headers=HEADERS).json()
    response = client.post("/v1/thread-rpg/execute", headers=HEADERS, json=request_body())
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["record_status"] == "generated"
    assert body["trace_kind"] == "thread_rpg.phase_results"
    assert [item[0] for item in body["trace"]] == [
        "observation:A", "observation:B", "conference", "matome",
    ]
    assert len(body["observations"]) == 2
    assert body["conference"] is not None and body["matome"] is not None
    assert body["evidence_ids"] == []
    assert "execution_id" not in body and "trace_id" not in body
    assert body["human_gate_required"] is True
    for name in ["execution_authorized", "publish_authorized", "merge_authorized", "decision_authority"]:
        assert body[name] is False
    assert api.runtime.store is store_before
    assert api.runtime.loop.state is state_before
    assert calls == [("prompt", "fixture")]
    assert client.get("/v1/evidence", headers=HEADERS, params={"protocol_id": "thread_rpg"}).json() == []
    assert client.get("/v1/traces/T1", headers=HEADERS).json() == trace_before
    assert client.get("/v1/witnesses/T1/history", headers=HEADERS).json() == witness_before
    assert client.get("/v1/traceability/T1", headers=HEADERS).json()["valid"] is True


@pytest.mark.parametrize("perspectives", [[], [{"id": "A"}], [{"id": "A"}, {"id": "A"}]])
def test_invalid_perspectives_rejected_before_backend_call(perspectives):
    calls = []
    adapter = PipelineAdapter(lambda request: calls.append(request))
    client = TestClient(create_app(thread_rpg_adapter=adapter))
    response = client.post("/v1/thread-rpg/execute", json={**request_body(), "perspectives": perspectives})
    assert response.status_code == 422
    assert calls == []


def test_backend_failure_does_not_promote_partial_generation_or_disclose_details():
    calls = []

    def fail_at_conference(request):
        calls.append(request.phase)
        if request.phase == "conference":
            raise RuntimeError("sensitive provider details")
        return "generated observation"

    api = ShirakamiAPI()
    store_before = api.runtime.store
    state_before = api.runtime.loop.state
    client = TestClient(create_app(api=api, thread_rpg_adapter=PipelineAdapter(fail_at_conference)))
    response = client.post("/v1/thread-rpg/execute", json=request_body())
    assert response.status_code == 502
    assert "sensitive provider details" not in response.text
    assert calls == ["independent_observation", "independent_observation", "conference"]
    assert api.runtime.store is store_before
    assert api.runtime.loop.state is state_before

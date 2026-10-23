import json
import urllib.request

from runtime.adapter import PipelineAdapter
from runtime.pipeline import build_pipeline_plan
from runtime.pipeline_execution import execute_pipeline_plan
from runtime.protocol_api import build_protocol_request
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry
from runtime.umr_backend import UMRBackend


MATOME_YAML = """matome:
  title: UMR Live Pipeline E2E
  version: "0.1"
  statement: >
    Verify real HTTP execution for each pipeline step.
  pipeline:
    - phase: observe
      action: inspect
    - phase: organize
      action: structure
"""


def test_pipeline_sends_each_step_to_live_umr_server():
    health_url = "http://127.0.0.1:8766/health"
    with urllib.request.urlopen(health_url, timeout=3) as response:
        health = json.loads(response.read().decode("utf-8"))

    assert health["status"] == "ok"
    assert health["service"] == "UMR"

    protocol = parse_matome(MATOME_YAML)
    plan = build_pipeline_plan(protocol, {"source": "live-e2e-test"})

    registry = ProtocolRegistry()
    registry.register_temporary(protocol.protocol_id, protocol)

    request = build_protocol_request(
        registry,
        protocol.protocol_id,
        {"task": "Verify real HTTP pipeline execution"},
    )

    umr = UMRBackend(
        base_url="http://127.0.0.1:8766",
        engine="mock",
        timeout=10,
    )

    def execute_step(adapter_request):
        response = umr.execute(
            {
                "input": {
                    "task": dict(adapter_request.input),
                    "phase": adapter_request.phase,
                    "action": adapter_request.action,
                },
                "context_bundle": dict(adapter_request.context),
                "previous_outputs": [
                    {
                        "output": result.output,
                        "backend": result.backend,
                        "evidence": dict(result.evidence),
                    }
                    for result in adapter_request.previous_outputs
                ],
            }
        )

        return {
            "backend_id": response.backend_id,
            "status": response.status,
            "output": response.payload["output"],
        }

    adapter = PipelineAdapter(
        execute_step,
        backend_id=umr.backend_id,
    )

    trace = execute_pipeline_plan(request, plan, adapter)

    assert trace.completed is True
    assert trace.protocol_id == protocol.protocol_id
    assert trace.version == protocol.version
    assert len(trace.steps) == 2
    assert trace.backends == (umr.backend_id, umr.backend_id)

    echoed_inputs = []
    for step in trace.steps:
        assert step.output["status"] == "completed"
        assert step.output["backend_id"] == umr.backend_id
        assert isinstance(step.output["output"], dict)
        assert isinstance(step.output["output"]["text"], str)
        echoed_inputs.append(
            json.loads(step.output["output"]["text"])
        )

    assert [
        item["task_input"]["phase"]
        for item in echoed_inputs
    ] == ["observe", "organize"]

    assert [
        item["task_input"]["action"]
        for item in echoed_inputs
    ] == ["inspect", "structure"]

    assert all(
        item["task_input"]["task"] == {
            "task": "Verify real HTTP pipeline execution"
        }
        for item in echoed_inputs
    )

    assert all(
        item["context_bundle"]["source"] == "live-e2e-test"
        for item in echoed_inputs
    )

    assert echoed_inputs[0]["previous_outputs"] == []
    assert len(echoed_inputs[1]["previous_outputs"]) == 1

    first_result = echoed_inputs[1]["previous_outputs"][0]["output"]
    assert first_result["status"] == "completed"
    assert first_result["backend_id"] == umr.backend_id

    first_model_input = json.loads(first_result["output"]["text"])
    assert first_model_input["task_input"]["phase"] == "observe"
    assert first_model_input["task_input"]["action"] == "inspect"

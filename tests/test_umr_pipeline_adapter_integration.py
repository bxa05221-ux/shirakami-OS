import json

from runtime.adapter import PipelineAdapter
from runtime.pipeline import build_pipeline_plan
from runtime.pipeline_execution import execute_pipeline_plan
from runtime.protocol_api import build_protocol_request
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry
from runtime.umr_backend import UMRBackend


MATOME_YAML = """matome:
  title: UMR Pipeline Adapter Integration
  version: "0.1"
  statement: >
    Verify that each pipeline step reaches the replaceable UMR backend.
  pipeline:
    - phase: observe
      action: inspect
    - phase: organize
      action: structure
"""


def test_pipeline_adapter_calls_umr_for_each_step():
    protocol = parse_matome(MATOME_YAML)
    plan = build_pipeline_plan(protocol, {"source": "integration-test"})

    registry = ProtocolRegistry()
    registry.register_temporary(protocol.protocol_id, protocol)

    request = build_protocol_request(
        registry,
        protocol.protocol_id,
        {"task": "Preserve the execution boundary"},
    )

    captured = []

    def mock_umr_transport(http_request, timeout):
        body = json.loads(http_request.data.decode("utf-8"))
        captured.append(body)

        return json.dumps(
            {
                "status": "success",
                "engine": body["engine"],
                "output": {"text": body["input"]["text"]},
                "error": None,
            }
        ).encode("utf-8")

    umr = UMRBackend(
        engine="mock",
        transport=mock_umr_transport,
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
    assert len(captured) == 2

    decoded_inputs = [
        json.loads(body["input"]["text"])
        for body in captured
    ]

    assert [
        item["task_input"]["phase"]
        for item in decoded_inputs
    ] == ["observe", "organize"]

    assert [
        item["task_input"]["action"]
        for item in decoded_inputs
    ] == ["inspect", "structure"]

    assert all(
        item["task_input"]["task"] == {
            "task": "Preserve the execution boundary"
        }
        for item in decoded_inputs
    )

    assert all(
        item["context_bundle"]["source"] == "integration-test"
        for item in decoded_inputs
    )

    assert decoded_inputs[0]["previous_outputs"] == []

    second_step_previous = decoded_inputs[1]["previous_outputs"]
    assert len(second_step_previous) == 1

    first_result = second_step_previous[0]["output"]
    assert first_result["status"] == "completed"
    assert first_result["backend_id"] == umr.backend_id

    first_model_input = json.loads(first_result["output"]["text"])
    assert first_model_input["task_input"]["phase"] == "observe"
    assert first_model_input["task_input"]["action"] == "inspect"

    for step in trace.steps:
        assert step.output["status"] == "completed"
        assert step.output["backend_id"] == umr.backend_id
        assert "judgment" not in step.output
        assert "decision" not in step.output

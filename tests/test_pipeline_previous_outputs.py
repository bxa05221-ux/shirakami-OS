from runtime.adapter import PipelineAdapter
from runtime.pipeline import build_pipeline_plan
from runtime.pipeline_execution import execute_pipeline_plan
from runtime.protocol_api import ProtocolRequest
from runtime.protocol_loader import parse_matome


def test_pipeline_passes_prior_outputs_without_mutating_input():
    protocol = parse_matome(
        """matome:
  title: Pipeline Previous Outputs Test
  version: "0.1"
  statement: >
    Verify previous step output handoff.
  pipeline:
    - phase: observe
      action: inspect
    - phase: organize
      action: structure
    - phase: reflect
      action: review
"""
    )

    original_input = {"task": "keep this input"}
    original_context = {"source": "previous-output-test"}

    request = ProtocolRequest(
        protocol_id=protocol.protocol_id,
        version=protocol.version,
        input=original_input,
    )
    plan = build_pipeline_plan(protocol, original_context)

    seen_requests = []

    def backend(adapter_request):
        seen_requests.append(adapter_request)
        return {
            "phase": adapter_request.phase,
            "result": f"result-{adapter_request.phase}",
        }

    adapter = PipelineAdapter(backend, backend_id="test-backend")
    trace = execute_pipeline_plan(request, plan, adapter)

    assert trace.completed is True
    assert len(trace.steps) == 3
    assert [len(item.previous_outputs) for item in seen_requests] == [0, 1, 2]

    assert seen_requests[1].previous_outputs[0].output == {
        "phase": "observe",
        "result": "result-observe",
    }

    assert [
        item.output["phase"]
        for item in seen_requests[2].previous_outputs
    ] == ["observe", "organize"]

    for adapter_request in seen_requests:
        assert dict(adapter_request.input) == original_input
        assert dict(adapter_request.context) == original_context
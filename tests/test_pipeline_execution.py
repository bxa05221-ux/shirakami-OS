from runtime.pipeline import PipelinePlan, PipelineStep
from runtime.pipeline_execution import execute_pipeline_plan
from runtime.protocol_api import ProtocolRequest
from runtime.adapter import PipelineAdapter


def test_execute_pipeline_plan_preserves_step_order_and_backend():
    seen = []

    def backend(request):
        seen.append((request.phase, request.action, request.context["time"]))
        return {"status": "ok", "phase": request.phase}

    request = ProtocolRequest(
        protocol_id="writing",
        version="0.1",
        input={"canonical_prompt": "文章を整理する"},
    )
    plan = PipelinePlan(
        protocol_id="writing",
        version="0.1",
        steps=(
            PipelineStep(phase="observe", action="inspect"),
            PipelineStep(phase="organize", action="structure"),
        ),
        context={"time": "night"},
    )

    trace = execute_pipeline_plan(request, plan, PipelineAdapter(backend, backend_id="test-ai"))

    assert seen == [("observe", "inspect", "night"), ("organize", "structure", "night")]
    assert trace.backends == ("test-ai", "test-ai")
    assert trace.completed is True
    assert len(trace.steps) == 2


def test_execute_pipeline_plan_rejects_mismatched_protocol():
    request = ProtocolRequest(protocol_id="a", version="0.1", input={})
    plan = PipelinePlan(protocol_id="b", version="0.1", steps=(), context={})

    try:
        execute_pipeline_plan(request, plan, PipelineAdapter(lambda _: {}))
    except ValueError as error:
        assert "protocol_id" in str(error)
    else:
        raise AssertionError("expected protocol mismatch to fail")

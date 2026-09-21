from runtime.adapter import PipelineAdapter, PipelineAdapterRequest
from runtime.pipeline import build_pipeline_plan
from runtime.protocol_loader import parse_matome


def test_protocol_pipeline_adapter_backend_end_to_end():
    protocol = parse_matome(
        """matome:
  title: "文章作成"
  version: "0.1"
  statement: >
    文章を整理して編集する。
  pipeline:
    - phase: observe
      action: inspect
    - phase: organize
      action: structure
"""
    )
    plan = build_pipeline_plan(protocol, {"time": "night"})
    calls = []

    def backend(request):
        calls.append(request)
        return {"status": "ok", "action": request.action}

    adapter = PipelineAdapter(backend, backend_id="test-backend")
    results = []

    for step in plan.steps:
        results.append(
            adapter.execute(
                PipelineAdapterRequest(
                    protocol_id=plan.protocol_id,
                    version=plan.version,
                    phase=step.phase,
                    action=step.action,
                    input={"prompt": "文章を整理して"},
                    context=plan.context,
                )
            )
        )

    assert [request.phase for request in calls] == ["observe", "organize"]
    assert [request.action for request in calls] == ["inspect", "structure"]
    assert all(result.backend == "test-backend" for result in results)
    assert results[-1].output["status"] == "ok"

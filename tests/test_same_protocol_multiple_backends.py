from runtime.adapter import PipelineAdapter, PipelineAdapterRequest
from runtime.pipeline import build_pipeline_plan
from runtime.protocol_loader import parse_matome


def test_same_protocol_can_use_different_backends():
    protocol = parse_matome(
        """matome:
  title: "文章作成"
  version: "0.1"
  statement: >
    文章を整理して編集する。
  pipeline:
    - phase: observe
      action: inspect
"""
    )
    plan = build_pipeline_plan(protocol, {"time": "night"})

    def backend_a(request):
        return {"backend": "A", "action": request.action}

    def backend_b(request):
        return {"backend": "B", "action": request.action}

    adapters = [
        PipelineAdapter(backend_a, backend_id="backend-a"),
        PipelineAdapter(backend_b, backend_id="backend-b"),
    ]

    results = [
        adapter.execute(
            PipelineAdapterRequest(
                protocol_id=plan.protocol_id,
                version=plan.version,
                phase=plan.steps[0].phase,
                action=plan.steps[0].action,
                input={"prompt": "文章を整理して"},
                context=plan.context,
            )
        )
        for adapter in adapters
    ]

    assert plan.protocol_id == results[0].evidence["protocol_id"]
    assert results[0].backend == "backend-a"
    assert results[1].backend == "backend-b"
    assert results[0].evidence["action"] == results[1].evidence["action"]
    assert results[0].output["backend"] != results[1].output["backend"]

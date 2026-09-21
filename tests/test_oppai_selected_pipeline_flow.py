from runtime.adapter import PipelineAdapter
from runtime.oppai_runtime_flow import execute_selected_pipeline
from runtime.protocol_api import register_temporary_matome
from runtime.protocol_registry import ProtocolRegistry


def test_oppai_to_selected_protocol_pipeline_adapter_vertical_flow():
    registry = ProtocolRegistry()
    entry = register_temporary_matome(
        registry,
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
""",
    )

    seen = []

    def backend(request):
        seen.append((request.protocol_id, request.version, request.phase, request.action))
        return {"status": "ok", "phase": request.phase}

    result = execute_selected_pipeline(
        "文章を整理して",
        registry,
        entry.protocol_id,
        PipelineAdapter(backend, backend_id="test-backend"),
        context={"time": "night"},
    )

    assert result.request.protocol_id == entry.protocol_id
    assert result.plan.protocol_id == entry.protocol_id
    assert [step.phase for step in result.plan.steps] == ["observe", "organize"]
    assert [item.backend for item in result.steps] == ["test-backend", "test-backend"]
    assert seen == [
        (entry.protocol_id, "0.1", "observe", "inspect"),
        (entry.protocol_id, "0.1", "organize", "structure"),
    ]

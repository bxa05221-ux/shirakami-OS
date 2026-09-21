from runtime.adapter import PipelineAdapter, PipelineAdapterRequest


def test_pipeline_adapter_passes_step_to_backend():
    seen = []

    def backend(request):
        seen.append(request)
        return "ok"

    adapter = PipelineAdapter(backend, backend_id="test-backend")
    result = adapter.execute(
        PipelineAdapterRequest(
            protocol_id="writing",
            version="0.1",
            phase="observe",
            action="inspect",
            input={"prompt": "文章"},
            context={"time": "night"},
        )
    )

    assert result.output == "ok"
    assert result.backend == "test-backend"
    assert seen[0].phase == "observe"
    assert seen[0].action == "inspect"
    assert result.evidence["backend_declared"] is True


def test_pipeline_adapter_does_not_select_backend():
    adapter = PipelineAdapter(lambda request: "ok")
    result = adapter.execute(
        PipelineAdapterRequest(
            protocol_id="writing",
            version="0.1",
            phase="observe",
            action="inspect",
            input={},
            context={},
        )
    )

    assert result.backend is None

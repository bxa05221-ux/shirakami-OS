from runtime.adapter import PipelineAdapter, PipelineAdapterResult
from runtime.thread_rpg_execution import (
    ThreadRPGExecutionError,
    execute_thread_rpg,
)


def test_thread_rpg_runs_independent_observations_then_conference_and_matome():
    calls = []

    def backend(request):
        calls.append(request)
        return {
            "phase": request.phase,
            "perspective_id": request.context.get("perspective_id"),
            "previous_count": len(request.previous_outputs),
        }

    adapter = PipelineAdapter(backend, backend_id="test-backend")

    result = execute_thread_rpg(
        task={"question": "What happened?"},
        perspectives=[
            {"id": "A", "viewpoint": "first viewpoint"},
            {"id": "B", "viewpoint": "second viewpoint"},
        ],
        adapter=adapter,
        context={"source": "test"},
    )

    assert [call.phase for call in calls] == [
        "independent_observation",
        "independent_observation",
        "conference",
        "matome",
    ]
    assert calls[0].context["perspective_id"] == "A"
    assert calls[1].context["perspective_id"] == "B"
    assert calls[0].previous_outputs == ()
    assert calls[1].previous_outputs == ()
    assert len(calls[2].previous_outputs) == 2
    assert len(calls[3].previous_outputs) == 3

    assert result.perspective_ids == ("A", "B")
    assert len(result.observations) == 2
    assert result.conference.output["phase"] == "conference"
    assert result.matome.output["phase"] == "matome"
    assert [name for name, _ in result.trace] == [
        "observation:A",
        "observation:B",
        "conference",
        "matome",
    ]


def test_thread_rpg_rejects_fewer_than_two_perspectives():
    adapter = PipelineAdapter(lambda request: "unused")

    try:
        execute_thread_rpg(
            task={"question": "test"},
            perspectives=[{"id": "A"}],
            adapter=adapter,
        )
    except ThreadRPGExecutionError as exc:
        assert "at least two perspectives" in str(exc)
    else:
        raise AssertionError("expected ThreadRPGExecutionError")


def test_thread_rpg_rejects_duplicate_perspective_ids():
    adapter = PipelineAdapter(lambda request: "unused")

    try:
        execute_thread_rpg(
            task={"question": "test"},
            perspectives=[{"id": "A"}, {"id": "A"}],
            adapter=adapter,
        )
    except ThreadRPGExecutionError as exc:
        assert "duplicate perspective id" in str(exc)
    else:
        raise AssertionError("expected ThreadRPGExecutionError")

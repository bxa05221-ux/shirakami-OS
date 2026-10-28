import json

from runtime.adapter import PipelineAdapter
from runtime.thread_rpg_execution import execute_thread_rpg
from runtime.umr_backend import UMRBackend


def test_thread_rpg_execution_integrates_with_umr_backend():
    captured = []

    def mock_transport(request, timeout):
        body = json.loads(request.data.decode("utf-8"))
        captured.append(body)
        model_input = json.loads(body["input"]["text"])

        output = {
            "phase": model_input["task_input"]["phase"],
            "marker": f"stage-{len(captured)}",
        }

        return json.dumps({
            "status": "success",
            "engine": body["engine"],
            "output": output,
            "error": None,
        }).encode("utf-8")

    umr = UMRBackend(engine="mock", transport=mock_transport)

    def execute_step(request):
        response = umr.execute({
            "input": {
                "task": dict(request.input),
                "phase": request.phase,
                "action": request.action,
            },
            "context_bundle": dict(request.context),
            "previous_outputs": [
                {
                    "output": result.output,
                    "backend": result.backend,
                    "evidence": dict(result.evidence),
                }
                for result in request.previous_outputs
            ],
        })

        return {
            "backend_id": response.backend_id,
            "status": response.status,
            "output": response.payload["output"],
        }

    adapter = PipelineAdapter(
        execute_step,
        backend_id=umr.backend_id,
    )

    result = execute_thread_rpg(
        task={"question": "Explore different interpretations"},
        perspectives=[
            {"id": "A", "viewpoint": "viewpoint A"},
            {"id": "B", "viewpoint": "viewpoint B"},
        ],
        adapter=adapter,
        context={"source": "thread-rpg-umr-integration-test"},
    )

    assert len(captured) == 4
    assert [step[0] for step in result.trace] == [
        "observation:A",
        "observation:B",
        "conference",
        "matome",
    ]

    decoded = [
        json.loads(body["input"]["text"])
        for body in captured
    ]

    assert [
        item["task_input"]["phase"]
        for item in decoded
    ] == [
        "independent_observation",
        "independent_observation",
        "conference",
        "matome",
    ]

    assert decoded[0]["previous_outputs"] == []
    assert decoded[1]["previous_outputs"] == []
    assert len(decoded[2]["previous_outputs"]) == 2
    assert len(decoded[3]["previous_outputs"]) == 3

    assert decoded[0]["task_input"]["task"]["perspective"]["id"] == "A"
    assert decoded[1]["task_input"]["task"]["perspective"]["id"] == "B"

    assert all(
        item["context_bundle"]["source"]
        == "thread-rpg-umr-integration-test"
        for item in decoded
    )

    assert all(
        step.output["status"] == "completed"
        for _, step in result.trace
    )
    assert all(
        step.output["backend_id"] == umr.backend_id
        for _, step in result.trace
    )
    # This orchestration returns a trace; it does not make a decision or
    # update Landscape.
    assert result.matome.output["output"]["phase"] == "matome"

from runtime.activation_pump import ReleasedActivation
from runtime.evidence_landscape_projection import project_evidence
from runtime.landscape import LandscapeState
from runtime.pipeline_runner import (
    PipelineRunnerError,
    run_approved_pipeline_on_runner,
)


def activation(name: str) -> ReleasedActivation:
    return ReleasedActivation(
        activation_id=f"activation-{name}",
        candidate_id=f"candidate-{name}",
        protocol_id=f"protocol-{name}",
        approval_reviewer="human-1",
    )


def test_pipeline_runs_each_activation_through_existing_runner_and_preserves_order():
    activations = (activation("a"), activation("b"))
    executed = []

    result = run_approved_pipeline_on_runner(
        pipeline_identity="pipeline-1",
        activations=activations,
        iteration_budget=1,
        execute=lambda current, iteration: executed.append(current.activation_id) or True,
        verify=lambda current, iteration: True,
    )

    assert result.stopped is False
    assert executed == ["activation-a", "activation-b"]
    assert {item.execution_order for item in result.items} == {1, 2}
    assert {item.run_identity for item in result.items} == {
        "pipeline-1:run:1",
        "pipeline-1:run:2",
    }
    assert {item.activation_identity for item in result.items} == {
        "activation-a",
        "activation-b",
    }
    assert all(item.pipeline_identity == "pipeline-1" for item in result.items)
    assert all(
        item.evidence.transition_data["pipeline_identity"] == "pipeline-1"
        for item in result.items
    )


def test_verification_mismatch_stops_later_pipeline_items():
    activations = (activation("a"), activation("b"))
    executed = []

    result = run_approved_pipeline_on_runner(
        pipeline_identity="pipeline-2",
        activations=activations,
        iteration_budget=1,
        execute=lambda current, iteration: executed.append(current.activation_id) or True,
        verify=lambda current, iteration: False,
    )

    assert result.stopped is True
    assert executed == ["activation-a"]
    assert {item.activation_identity for item in result.items} == {"activation-a"}
    assert result.runner_results[0].state.value == "STOPPED"


def test_runner_evidence_remains_observation_and_does_not_project_to_landscape():
    result = run_approved_pipeline_on_runner(
        pipeline_identity="pipeline-3",
        activations=(activation("a"),),
        iteration_budget=1,
        execute=lambda current, iteration: True,
        verify=lambda current, iteration: True,
    )

    landscape = LandscapeState.empty()
    before = landscape.snapshot()

    for item in result.items:
        project_evidence(item.evidence, landscape)

    assert landscape.snapshot() == before


def test_pipeline_identity_and_order_are_not_authority():
    result = run_approved_pipeline_on_runner(
        pipeline_identity="pipeline-4",
        activations=(activation("a"),),
        iteration_budget=1,
        execute=lambda current, iteration: True,
        verify=lambda current, iteration: True,
    )

    assert all(not getattr(item.evidence, "authority", False) for item in result.items)
    assert all(item.evidence.transition_data["execution_order"] == 1 for item in result.items)


def test_missing_pipeline_identity_fails_closed():
    try:
        run_approved_pipeline_on_runner(
            pipeline_identity="",
            activations=(activation("a"),),
            iteration_budget=1,
            execute=lambda current, iteration: True,
            verify=lambda current, iteration: True,
        )
    except PipelineRunnerError:
        return
    raise AssertionError("missing pipeline identity must fail closed")


def test_non_released_activation_fails_closed():
    try:
        run_approved_pipeline_on_runner(
            pipeline_identity="pipeline-5",
            activations=(object(),),
            iteration_budget=1,
            execute=lambda current, iteration: True,
            verify=lambda current, iteration: True,
        )
    except PipelineRunnerError:
        return
    raise AssertionError("non-ReleasedActivation must fail closed")

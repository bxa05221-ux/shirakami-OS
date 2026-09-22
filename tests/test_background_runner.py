import pytest

from runtime.activation import Activation
from runtime.activation_pump import release_activation
from runtime.background_runner import BackgroundRunnerError, RunnerState, run_released_activation


def released():
    return release_activation(
        activation=Activation(
            candidate_id="candidate-test-001",
            protocol_id="protocol-test-001",
            approval_reviewer="human-test",
            activation_id="activation-test-001",
        ),
        release_id="release-test-001",
    )


def test_runner_executes_within_budget_and_preserves_identity():
    calls = []
    result = run_released_activation(
        activation=released(),
        iteration_budget=3,
        run_id="run-test-001",
        execute=lambda activation, iteration: calls.append(iteration) or iteration == 2,
        verify=lambda activation, iteration: True,
    )
    assert calls == [1, 2]
    assert result.state is RunnerState.COMPLETED
    assert result.protocol_identity == "protocol-test-001"
    assert result.activation_identity == "activation-test-001"
    assert result.approval_identity == "human-test"
    assert result.run_identity == "run-test-001"


def test_runner_stops_on_budget_exhaustion():
    result = run_released_activation(
        activation=released(), iteration_budget=2, run_id="run-test-002",
        execute=lambda activation, iteration: False,
        verify=lambda activation, iteration: True,
    )
    assert result.state is RunnerState.STOPPED
    assert result.iterations == 2
    assert result.events[-1].event == "runner_stopped"


def test_runner_stops_on_verification_mismatch():
    result = run_released_activation(
        activation=released(), iteration_budget=3, run_id="run-test-003",
        execute=lambda activation, iteration: True,
        verify=lambda activation, iteration: False,
    )
    assert result.state is RunnerState.STOPPED
    assert [event.event for event in result.events][-2:] == ["verification_requested", "runner_stopped"]


@pytest.mark.parametrize("bad_budget", [0, -1, True, 1.5, "1"])
def test_runner_fails_closed_on_invalid_budget(bad_budget):
    with pytest.raises(BackgroundRunnerError):
        run_released_activation(
            activation=released(), iteration_budget=bad_budget, run_id="run-test-004",
            execute=lambda activation, iteration: True,
            verify=lambda activation, iteration: True,
        )


def test_runner_requires_released_activation():
    with pytest.raises(BackgroundRunnerError):
        run_released_activation(
            activation=None, iteration_budget=1, run_id="run-test-005",
            execute=lambda activation, iteration: True,
            verify=lambda activation, iteration: True,
        )


def test_runner_requires_run_identity():
    with pytest.raises(BackgroundRunnerError):
        run_released_activation(
            activation=released(), iteration_budget=1, run_id="",
            execute=lambda activation, iteration: True,
            verify=lambda activation, iteration: True,
        )


def test_runner_requires_verification_callback():
    with pytest.raises(TypeError):
        run_released_activation(
            activation=released(), iteration_budget=1, run_id="run-test-006",
            execute=lambda activation, iteration: True,
        )


def test_runner_creates_no_authority():
    result = run_released_activation(
        activation=released(), iteration_budget=1, run_id="run-test-007",
        execute=lambda activation, iteration: True,
        verify=lambda activation, iteration: True,
    )
    assert not hasattr(result, "approval_envelope")
    assert not hasattr(result, "authority")

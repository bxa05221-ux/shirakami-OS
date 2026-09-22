"""Bounded Persistent Background Runner for released Shirakami Activations."""

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from runtime.activation_pump import ReleasedActivation


class BackgroundRunnerError(ValueError):
    """Raised when the runner cannot safely continue."""


class RunnerState(str, Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class RunnerEvent:
    event: str
    protocol_identity: str
    activation_identity: str
    approval_identity: str
    run_identity: str
    iteration: int
    runner_state: RunnerState


@dataclass(frozen=True)
class RunnerResult:
    run_identity: str
    protocol_identity: str
    activation_identity: str
    approval_identity: str
    iterations: int
    state: RunnerState
    events: tuple[RunnerEvent, ...]


def run_released_activation(
    *,
    activation: ReleasedActivation,
    iteration_budget: int,
    run_id: str,
    execute: Callable[[ReleasedActivation, int], bool],
    verify: Callable[[ReleasedActivation, int], bool],
) -> RunnerResult:
    """Execute a released Activation within an explicit bounded budget."""
    _validate_input(activation, iteration_budget, run_id)

    events: list[RunnerEvent] = [
        RunnerEvent("runner_started", activation.protocol_id, activation.activation_id,
                    activation.approval_reviewer, run_id, 0, RunnerState.READY)
    ]

    for iteration in range(1, iteration_budget + 1):
        events.append(_event("iteration_started", activation, run_id, iteration, RunnerState.RUNNING))
        try:
            completed = execute(activation, iteration)
        except Exception as exc:
            events.append(_event("runner_failed", activation, run_id, iteration, RunnerState.FAILED))
            raise BackgroundRunnerError("execution failed") from exc

        events.append(_event("iteration_completed", activation, run_id, iteration, RunnerState.RUNNING))

        if completed:
            events.append(_event("verification_requested", activation, run_id, iteration, RunnerState.VERIFYING))
            try:
                verified = verify(activation, iteration)
            except Exception as exc:
                events.append(_event("runner_failed", activation, run_id, iteration, RunnerState.FAILED))
                raise BackgroundRunnerError("verification failed") from exc

            if not verified:
                events.append(_event("runner_stopped", activation, run_id, iteration, RunnerState.STOPPED))
                return _result(activation, run_id, iteration, RunnerState.STOPPED, events)

            events.append(_event("runner_stopped", activation, run_id, iteration, RunnerState.COMPLETED))
            return _result(activation, run_id, iteration, RunnerState.COMPLETED, events)

    events.append(_event("runner_stopped", activation, run_id, iteration_budget, RunnerState.STOPPED))
    return _result(activation, run_id, iteration_budget, RunnerState.STOPPED, events)


def _validate_input(activation, iteration_budget: int, run_id: str) -> None:
    if not isinstance(activation, ReleasedActivation):
        raise BackgroundRunnerError("released activation is required")
    if activation.lifecycle_event != "activated_execution":
        raise BackgroundRunnerError("released activation is invalid")
    if not activation.protocol_id.strip():
        raise BackgroundRunnerError("protocol identity is required")
    if not activation.activation_id.strip():
        raise BackgroundRunnerError("activation identity is required")
    if not activation.approval_reviewer.strip():
        raise BackgroundRunnerError("approval identity is required")
    if not run_id.strip():
        raise BackgroundRunnerError("run identity is required")
    if isinstance(iteration_budget, bool) or not isinstance(iteration_budget, int) or iteration_budget <= 0:
        raise BackgroundRunnerError("iteration budget must be a positive integer")


def _event(name, activation, run_id, iteration, state):
    return RunnerEvent(name, activation.protocol_id, activation.activation_id,
                       activation.approval_reviewer, run_id, iteration, state)


def _result(activation, run_id, iterations, state, events):
    return RunnerResult(run_id, activation.protocol_id, activation.activation_id,
                        activation.approval_reviewer, iterations, state, tuple(events))

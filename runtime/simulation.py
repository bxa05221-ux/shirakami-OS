"""Prompt -> Runtime -> Simulation boundary for Shirakami MVP.

The boundary deliberately executes a supplied simulation callable instead of
calling an external AI provider. The result is observable and can be handed
to AIwitness.
"""

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .prompt import PromptSpec


@dataclass(frozen=True)
class SimulationResult:
    simulation_id: str
    prompt_id: str
    protocol_id: str
    status: str
    output: Mapping[str, Any]
    assumptions: tuple[str, ...] = ()


Simulation = Callable[[PromptSpec], Mapping[str, Any]]


def execute_simulation(
    prompt: PromptSpec,
    simulation: Simulation,
    *,
    simulation_id: str,
) -> SimulationResult:
    """Execute one bounded simulation and return an inspectable result."""
    if not isinstance(prompt, PromptSpec):
        raise TypeError("prompt must be PromptSpec")
    if not callable(simulation):
        raise TypeError("simulation must be callable")

    try:
        output = simulation(prompt)
    except Exception as exc:
        return SimulationResult(
            simulation_id=simulation_id,
            prompt_id=prompt.prompt_id,
            protocol_id=prompt.protocol_id,
            status="failed",
            output={
                "error_type": type(exc).__name__,
                "message": str(exc),
            },
        )

    if not isinstance(output, Mapping):
        return SimulationResult(
            simulation_id=simulation_id,
            prompt_id=prompt.prompt_id,
            protocol_id=prompt.protocol_id,
            status="failed",
            output={
                "error_type": "InvalidSimulationResult",
                "message": "simulation must return a mapping",
            },
        )

    return SimulationResult(
        simulation_id=simulation_id,
        prompt_id=prompt.prompt_id,
        protocol_id=prompt.protocol_id,
        status="completed",
        output=dict(output),
    )


def capture_simulation_evidence(result: SimulationResult) -> dict[str, Any]:
    """Represent Simulation as a separate evidence object, never as Reality."""
    return {
        "simulation_id": result.simulation_id,
        "prompt_id": result.prompt_id,
        "protocol_id": result.protocol_id,
        "status": result.status,
        "output": dict(result.output),
        "kind": "simulation",
    }

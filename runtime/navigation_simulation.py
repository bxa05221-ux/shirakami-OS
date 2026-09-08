"""Minimal scenario projection for navigation state.

Projection is a conditional simulation, not a prediction. It extends
observed navigation state without selecting destinations, values, or truth.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .navigation import NavigationState


@dataclass(frozen=True)
class NavigationScenario:
    """One projected navigation state at a future step."""

    step: int
    state: Mapping[str, Any]
    basis: str = "continue_observed_direction"


class NavigationSimulator:
    """Project the current navigation state without autonomous steering."""

    def project(self, state: NavigationState, *, steps: int = 1) -> list[NavigationScenario]:
        if not isinstance(steps, int) or steps < 1:
            raise ValueError("steps must be a positive integer")

        base = dict(state.snapshot())
        scenarios: list[NavigationScenario] = []
        for step in range(1, steps + 1):
            projected = dict(base)
            projected["projection_step"] = step
            projected["projection"] = "conditional"
            projected["basis"] = "continue_observed_direction"
            scenarios.append(
                NavigationScenario(
                    step=step,
                    state=projected,
                )
            )
        return scenarios

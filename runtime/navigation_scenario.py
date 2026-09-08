"""Small, explicit continuity scenarios for Shirakami navigation.

A scenario is a projection of observed state, not a prediction. It repeats
only the latest observed navigation values and labels the result as synthetic.
No destination, value, cause, or course correction is introduced.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class NavigationScenario:
    """Synthetic states produced by continuing the latest observation."""

    basis: Mapping[str, Any]
    steps: tuple[Mapping[str, Any], ...]
    assumption: str = "continue_latest_observed_state"

    @classmethod
    def continue_observed_state(
        cls,
        snapshot: Mapping[str, Any],
        *,
        steps: int = 3,
    ) -> "NavigationScenario":
        if steps < 1:
            raise ValueError("steps must be >= 1")
        basis = dict(snapshot)
        projected = []
        for index in range(1, steps + 1):
            state = dict(basis)
            state["projection_step"] = index
            state["synthetic"] = True
            projected.append(state)
        return cls(basis=basis, steps=tuple(projected))

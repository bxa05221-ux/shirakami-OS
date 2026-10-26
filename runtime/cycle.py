"""Minimal human-steered Landscape observation cycle for Shirakami OS.

The cycle is deliberately small: re-observe the current Landscape, offer a
Handle, let a human choose it, observe an explicit outcome, and return the
new Landscape. No step in this module chooses values, destinations, or
outcomes on behalf of the human.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .choice import HandleChoice, choose_handle
from .handle import Handle, offer_handle
from .observation import ObservationRequest, ObservationView
from .outcome import HandleOutcome, observe_handle_outcome


@dataclass(frozen=True)
class CycleStep:
    """The observable artifacts of one human-steered cycle before execution."""

    view: ObservationView
    handle: Handle
    choice: HandleChoice


def begin_cycle(
    landscape: Mapping[str, Any],
    request: ObservationRequest,
    *,
    label: str | None = None,
    actor: str = "human",
) -> CycleStep:
    """Create one observation -> handle -> human-choice step."""
    from .observation import reobserve

    view = reobserve(landscape, request)
    handle = offer_handle(view, label=label)
    choice = choose_handle(handle, actor=actor)
    return CycleStep(view=view, handle=handle, choice=choice)


def record_cycle_outcome(
    step: CycleStep,
    observed: Mapping[str, Any],
) -> HandleOutcome:
    """Record only an explicitly observed outcome for a chosen Handle."""
    if not isinstance(step, CycleStep):
        raise TypeError("step must be a CycleStep")
    return observe_handle_outcome(step.choice, observed)

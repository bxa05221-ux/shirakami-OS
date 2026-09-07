"""Protocol-neutral observe -> step -> re-observe service boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol

from .landscape import LandscapeState
from .way import SmallStep, SmallStepSelector


class LandscapeObserver(Protocol):
    def observe(self, state: LandscapeState) -> Mapping[str, object]:
        ...


class StepApplier(Protocol):
    def apply(self, state: LandscapeState, step: SmallStep) -> None:
        ...


@dataclass(frozen=True)
class WayfindingCycle:
    before: Mapping[str, object]
    step: SmallStep
    after: Mapping[str, object]


def execute_small_step(
    state: LandscapeState,
    selector: SmallStepSelector,
    applier: StepApplier,
    observer: LandscapeObserver,
) -> WayfindingCycle:
    """Select and apply one external Small Step, then observe again."""
    before = dict(observer.observe(state))
    step = selector.select(before)
    applier.apply(state, step)
    after = dict(observer.observe(state))
    return WayfindingCycle(before=before, step=step, after=after)

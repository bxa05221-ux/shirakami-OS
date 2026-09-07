"""User-facing AATS -> Landscape -> Small Step -> re-observation flow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol

from .aats import Thread
from .landscape import LandscapeState
from .way import Kasen, Renzan, SmallStep, SmallStepSelector


class LandscapeObserver(Protocol):
    def observe(self, state: LandscapeState) -> Mapping[str, object]:
        ...


class StepApplier(Protocol):
    def apply(self, state: LandscapeState, step: SmallStep) -> None:
        ...


@dataclass(frozen=True)
class AATSWayfindingResult:
    viewpoints: tuple[object, ...]
    narrative: str
    before: Mapping[str, object]
    small_step: SmallStep
    after: Mapping[str, object]


def run_aats_wayfinding(
    thread: Thread,
    state: LandscapeState,
    selector: SmallStepSelector,
    applier: StepApplier,
    observer: LandscapeObserver,
) -> AATSWayfindingResult:
    """Run one complete user-facing turn without embedding policy semantics."""
    viewpoints = Renzan().collect(thread)
    narrative = Kasen().compose(viewpoints)
    before = dict(observer.observe(state))
    small_step = selector.select(before)
    applier.apply(state, small_step)
    after = dict(observer.observe(state))
    return AATSWayfindingResult(
        viewpoints=viewpoints,
        narrative=narrative,
        before=before,
        small_step=small_step,
        after=after,
    )

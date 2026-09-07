"""Complete AATS Thread -> Landscape -> Small Step -> Evidence cycle."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol

from .aats import Thread
from .evidence import EvidenceRecord, capture_evidence
from .landscape import LandscapeState
from .prototype import ExecutionResult, Transition
from .way import Kasen, Renzan, SmallStep, SmallStepSelector


class LandscapeObserver(Protocol):
    def observe(self, state: LandscapeState) -> Mapping[str, object]:
        ...


class StepApplier(Protocol):
    def apply(self, step: SmallStep) -> Transition:
        """Return an observable transition for the selected step."""
        ...


@dataclass(frozen=True)
class AATSWayfindingResult:
    viewpoints: tuple[object, ...]
    narrative: str
    before: Mapping[str, object]
    small_step: SmallStep
    evidence: EvidenceRecord
    after: Mapping[str, object]


def run_aats_wayfinding(
    thread: Thread,
    state: LandscapeState,
    selector: SmallStepSelector,
    applier: StepApplier,
    observer: LandscapeObserver,
) -> AATSWayfindingResult:
    """Run one complete user-facing turn through the observable cycle."""
    viewpoints = Renzan().collect(thread)
    narrative = Kasen().compose(viewpoints)
    before = dict(observer.observe(state))

    small_step = selector.select(before)
    transition = applier.apply(small_step)
    result = ExecutionResult(
        status="completed",
        protocol_id="wayfinding.small_step",
        transition=transition,
        signals=("wayfinding.step.selected", "transition.observed"),
        steps=1,
    )
    evidence = capture_evidence(result)
    state.apply_evidence(evidence)
    after = dict(observer.observe(state))

    return AATSWayfindingResult(
        viewpoints=viewpoints,
        narrative=narrative,
        before=before,
        small_step=small_step,
        evidence=evidence,
        after=after,
    )

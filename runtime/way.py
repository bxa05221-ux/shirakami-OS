"""Service boundaries for the AATS -> viewpoint -> Small Step path."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol, Sequence

from .aats import Thread


@dataclass(frozen=True)
class Viewpoint:
    participant_id: str
    text: str
    aa: str | None = None


class Renzan:
    """Collect Thread posts as separate observable viewpoints."""

    def collect(self, thread: Thread) -> tuple[Viewpoint, ...]:
        return tuple(Viewpoint(p.participant_id, p.text, p.aa) for p in thread.posts)


class Kasen:
    """Human-facing re-expression boundary.

    The fallback preserves viewpoints while avoiding a dry participant
    transcript. Rich narrative generation can be supplied externally later.
    """

    def compose(self, viewpoints: Sequence[Viewpoint]) -> str:
        if not viewpoints:
            return ""
        if len(viewpoints) == 1:
            return viewpoints[0].text
        parts = [viewpoints[0].text]
        for viewpoint in viewpoints[1:]:
            parts.append(f"見方によっては、{viewpoint.text}とも考えられるかもしれません。")
        return " ".join(parts)


@dataclass(frozen=True)
class SmallStep:
    action: str
    reason: str | None = None


class SmallStepSelector(Protocol):
    def select(self, landscape: Mapping[str, object]) -> SmallStep:
        ...


@dataclass(frozen=True)
class WayfindingResult:
    landscape: Mapping[str, object]
    viewpoints: tuple[Viewpoint, ...]
    narrative: str
    small_step: SmallStep | None


def map_and_reexpress(landscape: Mapping[str, object], thread: Thread, *, selector: SmallStepSelector | None = None) -> WayfindingResult:
    """Map observable state and prepare it for externally selected Small Step."""
    viewpoints = Renzan().collect(thread)
    narrative = Kasen().compose(viewpoints)
    step = selector.select(landscape) if selector is not None else None
    return WayfindingResult(dict(landscape), viewpoints, narrative, step)

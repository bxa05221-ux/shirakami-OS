"""Service boundaries for the AATS -> viewpoint -> Small Step path.

This module deliberately contains no domain-truth engine. Renzan collects
observable viewpoints; Kasen re-expresses them for a human reader; the
wayfinding boundary accepts a current-state map and an externally selected
Small Step. Future cognitive protocols can implement the selector without
changing the AATS boundary.
"""

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
        return tuple(
            Viewpoint(
                participant_id=post.participant_id,
                text=post.text,
                aa=post.aa,
            )
            for post in thread.posts
        )


class Kasen:
    """Human-facing re-expression boundary for collected viewpoints.

    The default implementation intentionally avoids dry A/B attribution. It
    preserves the viewpoints while presenting them as a flowing set of
    possibilities. Rich narrative generation can be supplied by an external
    renderer/interpreter later.
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


def map_and_reexpress(
    landscape: Mapping[str, object],
    thread: Thread,
    *,
    selector: SmallStepSelector | None = None,
) -> WayfindingResult:
    """Map the current observable state and prepare it for Small Step selection."""
    viewpoints = Renzan().collect(thread)
    narrative = Kasen().compose(viewpoints)
    step = selector.select(landscape) if selector is not None else None
    return WayfindingResult(
        landscape=dict(landscape),
        viewpoints=viewpoints,
        narrative=narrative,
        small_step=step,
    )

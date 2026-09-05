"""Minimal non-directive handle boundary for Shirakami OS.

A Handle is a small invitation to inspect an available view. It does not
open the drawer, choose for the human, or mutate Landscape.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .observation import ObservationView


@dataclass(frozen=True)
class Handle:
    """A selectable handle placed beside an observation."""

    id: str
    label: str
    lens: str
    observed: Mapping[str, Any]
    uncertainty: tuple[Any, ...] = ()


def offer_handle(view: ObservationView, *, label: str | None = None) -> Handle:
    """Place a small, non-directive handle next to an observation view."""
    return Handle(
        id=f"handle:{view.lens}",
        label=label or f"{view.lens}から見てみる",
        lens=view.lens,
        observed=dict(view.observed),
        uncertainty=view.uncertainty,
    )


HANDLE_FORBIDDEN_OPERATIONS = frozenset(
    {
        "open_drawer",
        "choose_destination",
        "choose_values",
        "choose_faith",
        "make_decision",
        "mutate_landscape",
    }
)

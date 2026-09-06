from __future__ import annotations

from typing import Mapping

from .landscape import LandscapeState


def import_observation(observation: Mapping[str, object]) -> LandscapeState:
    """Import an adapter observation without assigning domain semantics."""
    snapshot = observation.get("snapshot")
    if not isinstance(snapshot, Mapping):
        raise ValueError("observation.snapshot must be a mapping")

    state = LandscapeState.empty()
    state._state.update(dict(snapshot))
    return state

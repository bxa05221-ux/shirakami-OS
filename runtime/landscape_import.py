from __future__ import annotations

from typing import Mapping

from .landscape import LandscapeState


def import_observation(observation: Mapping[str, object]) -> LandscapeState:
    """Bootstrap LandscapeState from an external observation snapshot."""
    snapshot = observation.get("snapshot")
    if not isinstance(snapshot, Mapping):
        raise ValueError("observation.snapshot must be a mapping")
    return LandscapeState.from_snapshot(snapshot)

"""Minimal temporal observation history for the Distorted Celestial Sphere boundary.

This module stores observations by stable star id. It does not infer meaning,
form constellations, or rank observations.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class StarObservation:
    star_id: str
    content: str
    distance: Any = None
    brightness: Any = None
    phase: Any = None


class StarObservationHistory:
    """Keep ordered observations for each explicitly supplied star id."""

    def __init__(self) -> None:
        self._history: dict[str, list[StarObservation]] = {}

    def record(self, observation: Mapping[str, Any]) -> StarObservation:
        star_id = observation.get("id")
        if not isinstance(star_id, str) or not star_id.strip():
            raise ValueError("star observation requires a non-empty id")

        item = StarObservation(
            star_id=star_id,
            content=str(observation.get("content", "")),
            distance=observation.get("distance"),
            brightness=observation.get("brightness"),
            phase=observation.get("phase"),
        )
        self._history.setdefault(star_id, []).append(item)
        return item

    def history(self, star_id: str) -> tuple[StarObservation, ...]:
        return tuple(self._history.get(star_id, ()))

    def star_ids(self) -> tuple[str, ...]:
        return tuple(self._history)

"""Navigation history and direction-trend observation for Shirakami OS.

This module records observed navigation states and describes changes across
observations. It does not infer causes, goals, values, or destinations.
"""

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class DirectionTrend:
    """A minimal description of how observed direction changed over time."""

    samples: tuple[Any, ...]
    changed: bool
    change_count: int


@dataclass
class NavigationHistory:
    """Ordered snapshots used to observe navigation movement."""

    snapshots: list[Mapping[str, Any]] = field(default_factory=list)

    def record(self, snapshot: Mapping[str, Any]) -> None:
        self.snapshots.append(dict(snapshot))

    def direction_trend(self) -> DirectionTrend:
        samples = tuple(snapshot.get("direction") for snapshot in self.snapshots)
        pairs = zip(samples, samples[1:])
        change_count = sum(1 for before, after in pairs if before != after)
        return DirectionTrend(
            samples=samples,
            changed=change_count > 0,
            change_count=change_count,
        )

    def latest(self) -> Mapping[str, Any] | None:
        return dict(self.snapshots[-1]) if self.snapshots else None

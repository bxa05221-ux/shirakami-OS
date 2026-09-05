"""Observable navigation changes for Shirakami OS.

A NavigationDelta describes only the difference between two observed
navigation states. It does not infer causes, goals, values, or a preferred
course.
"""

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class NavigationBeacon:
    """Immutable observation packet emitted from explicit navigation fields."""

    position: Any = None
    direction: Any = None
    attitude: Any = None
    horizon: Any = None
    uncertainty: tuple[Any, ...] = ()
    evidence_cursor: Any = None
    landscape_changed: bool = False

    def snapshot(self) -> Mapping[str, Any]:
        return {
            "position": self.position,
            "direction": self.direction,
            "attitude": self.attitude,
            "horizon": self.horizon,
            "uncertainty": list(self.uncertainty),
            "evidence_cursor": self.evidence_cursor,
            "landscape_changed": self.landscape_changed,
        }


@dataclass(frozen=True)
class NavigationDelta:
    """Immutable before/after observation difference."""

    before: Mapping[str, Any]
    after: Mapping[str, Any]
    changed_fields: tuple[str, ...]

    @classmethod
    def between(
        cls,
        before: Mapping[str, Any],
        after: Mapping[str, Any],
        *,
        fields: tuple[str, ...] = (
            "position",
            "direction",
            "attitude",
            "horizon",
            "landscape_revision",
            "evidence_cursor",
            "uncertainty",
        ),
    ) -> "NavigationDelta":
        changed = tuple(
            field
            for field in fields
            if before.get(field) != after.get(field)
        )
        return cls(dict(before), dict(after), changed)

    @property
    def changed(self) -> bool:
        return bool(self.changed_fields)

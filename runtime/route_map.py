"""Minimal Route Map for Protocol-to-Protocol navigation."""

from dataclasses import dataclass
from typing import Mapping


class RouteMapError(ValueError):
    """Raised when a Route Map cannot be constructed or queried."""


@dataclass(frozen=True)
class RouteMap:
    """Observable routing state independent of Protocol meaning."""

    current: str
    transitions: Mapping[str, tuple[str, ...]]

    @classmethod
    def from_mapping(cls, current: str, transitions: Mapping[str, object]) -> "RouteMap":
        if not current:
            raise RouteMapError("current protocol is required")
        normalized: dict[str, tuple[str, ...]] = {}
        for source, targets in transitions.items():
            if not isinstance(source, str) or not source:
                raise RouteMapError("route source must be a non-empty string")
            if not isinstance(targets, (list, tuple)):
                raise RouteMapError(f"route targets must be a sequence: {source}")
            if any(not isinstance(target, str) or not target for target in targets):
                raise RouteMapError(f"route target must be a non-empty string: {source}")
            normalized[source] = tuple(targets)
        return cls(current=current, transitions=normalized)

    def next_protocols(self) -> tuple[str, ...]:
        """Return Protocol IDs explicitly reachable from the current location."""
        return self.transitions.get(self.current, ())

    def can_transition(self, protocol_id: str) -> bool:
        """Return whether the current location explicitly permits a transition."""
        return protocol_id in self.next_protocols()

    def move(self, protocol_id: str) -> "RouteMap":
        """Advance along an explicitly declared edge."""
        if not self.can_transition(protocol_id):
            raise RouteMapError(
                f"protocol is not reachable from current route position: {protocol_id}"
            )
        return RouteMap(current=protocol_id, transitions=self.transitions)

    def record_transition(self, protocol_id: str) -> "RouteMap":
        """Record an observed move and make its destination current.

        No route is inferred or selected. The traversed edge is simply retained
        as observable route history.
        """
        if not isinstance(protocol_id, str) or not protocol_id:
            raise RouteMapError("protocol_id must be a non-empty string")
        updated = {source: tuple(targets) for source, targets in self.transitions.items()}
        targets = list(updated.get(self.current, ()))
        if protocol_id not in targets:
            targets.append(protocol_id)
        updated[self.current] = tuple(targets)
        return RouteMap(current=protocol_id, transitions=updated)

    def snapshot(self) -> dict[str, object]:
        """Return a plain observable Route Map representation."""
        return {
            "current": self.current,
            "transitions": {
                source: list(targets) for source, targets in self.transitions.items()
            },
        }

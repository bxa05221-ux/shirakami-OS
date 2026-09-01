"""Minimal protocol lifecycle registry for Shirakami OS.

Implementation-only lifecycle handling. This module does not interpret protocol
meaning; it only controls which registered artifacts are eligible as current.
"""

from dataclasses import dataclass
from typing import Any, Mapping


VALID_STATES = {"active", "experimental", "archived"}


class ProtocolRegistryError(ValueError):
    pass


@dataclass(frozen=True)
class RegistryEntry:
    protocol_id: str
    state: str
    artifact: Any


class ProtocolRegistry:
    def __init__(self) -> None:
        self._entries: dict[str, RegistryEntry] = {}

    def register(self, protocol_id: str, artifact: Any, state: str = "experimental") -> RegistryEntry:
        if not protocol_id:
            raise ProtocolRegistryError("protocol_id is required")
        if state not in VALID_STATES:
            raise ProtocolRegistryError(f"invalid protocol state: {state}")
        entry = RegistryEntry(protocol_id=protocol_id, state=state, artifact=artifact)
        self._entries[protocol_id] = entry
        return entry

    def get(self, protocol_id: str) -> RegistryEntry:
        try:
            return self._entries[protocol_id]
        except KeyError as exc:
            raise ProtocolRegistryError(f"unknown protocol: {protocol_id}") from exc

    def select_current(self, protocol_id: str) -> RegistryEntry:
        entry = self.get(protocol_id)
        if entry.state == "archived":
            raise ProtocolRegistryError(f"archived protocol cannot be current: {protocol_id}")
        return entry

    def set_state(self, protocol_id: str, state: str) -> RegistryEntry:
        if state not in VALID_STATES:
            raise ProtocolRegistryError(f"invalid protocol state: {state}")
        entry = self.get(protocol_id)
        updated = RegistryEntry(protocol_id=entry.protocol_id, state=state, artifact=entry.artifact)
        self._entries[protocol_id] = updated
        return updated

    def list_current_candidates(self) -> list[RegistryEntry]:
        return [entry for entry in self._entries.values() if entry.state != "archived"]

    def snapshot(self) -> Mapping[str, RegistryEntry]:
        return dict(self._entries)

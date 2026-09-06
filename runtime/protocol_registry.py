"""Protocol artifact registry with default and temporary lifecycles.

Implementation-only lifecycle handling. This module does not interpret protocol
meaning; it controls registration, replacement, selection, and removal.
"""

from dataclasses import dataclass
from typing import Any, Mapping


VALID_STATES = {"active", "experimental", "archived"}
VALID_LIFECYCLES = {"default", "temporary"}


class ProtocolRegistryError(ValueError):
    pass


@dataclass(frozen=True)
class RegistryEntry:
    protocol_id: str
    state: str
    artifact: Any
    lifecycle: str = "temporary"


class ProtocolRegistry:
    def __init__(self) -> None:
        self._entries: dict[str, RegistryEntry] = {}

    def register(
        self,
        protocol_id: str,
        artifact: Any,
        state: str = "experimental",
        lifecycle: str = "temporary",
    ) -> RegistryEntry:
        if not protocol_id:
            raise ProtocolRegistryError("protocol_id is required")
        if state not in VALID_STATES:
            raise ProtocolRegistryError(f"invalid protocol state: {state}")
        if lifecycle not in VALID_LIFECYCLES:
            raise ProtocolRegistryError(f"invalid protocol lifecycle: {lifecycle}")
        if lifecycle == "default" and any(
            entry.lifecycle == "default" for entry in self._entries.values()
            if entry.protocol_id != protocol_id
        ):
            raise ProtocolRegistryError("default protocol already exists")
        if lifecycle == "default" and state != "active":
            raise ProtocolRegistryError("default protocol must remain active")
        entry = RegistryEntry(
            protocol_id=protocol_id,
            state=state,
            artifact=artifact,
            lifecycle=lifecycle,
        )
        self._entries[protocol_id] = entry
        return entry

    def register_default(self, protocol_id: str, artifact: Any) -> RegistryEntry:
        """Register the one permanent default Protocol."""
        return self.register(
            protocol_id,
            artifact,
            state="active",
            lifecycle="default",
        )

    def register_temporary(
        self,
        protocol_id: str,
        artifact: Any,
        state: str = "experimental",
    ) -> RegistryEntry:
        """Register a user-authored temporary Protocol artifact."""
        return self.register(
            protocol_id,
            artifact,
            state=state,
            lifecycle="temporary",
        )

    def get(self, protocol_id: str) -> RegistryEntry:
        try:
            return self._entries[protocol_id]
        except KeyError as exc:
            raise ProtocolRegistryError(f"unknown protocol: {protocol_id}") from exc

    def get_default(self) -> RegistryEntry:
        for entry in self._entries.values():
            if entry.lifecycle == "default":
                return entry
        raise ProtocolRegistryError("default protocol is not registered")

    def require_default(self) -> RegistryEntry:
        """Require the OS-level default Protocol to exist."""
        return self.get_default()

    def select_current(self, protocol_id: str) -> RegistryEntry:
        entry = self.get(protocol_id)
        if entry.state == "archived":
            raise ProtocolRegistryError(f"archived protocol cannot be current: {protocol_id}")
        return entry

    def set_state(self, protocol_id: str, state: str) -> RegistryEntry:
        if state not in VALID_STATES:
            raise ProtocolRegistryError(f"invalid protocol state: {state}")
        entry = self.get(protocol_id)
        if entry.lifecycle == "default" and state != "active":
            raise ProtocolRegistryError("default protocol must remain active")
        updated = RegistryEntry(
            protocol_id=entry.protocol_id,
            state=state,
            artifact=entry.artifact,
            lifecycle=entry.lifecycle,
        )
        self._entries[protocol_id] = updated
        return updated

    def replace_temporary(self, protocol_id: str, artifact: Any) -> RegistryEntry:
        """Replace a temporary Protocol artifact without changing its identity."""
        entry = self.get(protocol_id)
        if entry.lifecycle != "temporary":
            raise ProtocolRegistryError("default protocol cannot be replaced as temporary")
        updated = RegistryEntry(
            protocol_id=entry.protocol_id,
            state=entry.state,
            artifact=artifact,
            lifecycle="temporary",
        )
        self._entries[protocol_id] = updated
        return updated

    def remove(self, protocol_id: str) -> None:
        """Remove a temporary Protocol; the default Protocol is permanent."""
        entry = self.get(protocol_id)
        if entry.lifecycle == "default":
            raise ProtocolRegistryError("default protocol cannot be removed")
        del self._entries[protocol_id]

    def list_current_candidates(self) -> list[RegistryEntry]:
        return [entry for entry in self._entries.values() if entry.state != "archived"]

    def snapshot(self) -> Mapping[str, RegistryEntry]:
        return dict(self._entries)

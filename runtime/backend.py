"""Vendor-neutral Backend contract for Shirakami Runtime β0.1."""

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


@dataclass(frozen=True)
class BackendResponse:
    """Backend output; no decision authority is implied."""

    backend_id: str
    status: str
    payload: Mapping[str, Any]


class Backend(Protocol):
    backend_id: str

    def execute(self, handoff: Mapping[str, Any]) -> BackendResponse:
        """Execute a handoff without creating or changing human authority."""
        ...


class EchoBackend:
    """Reference backend for replaceability and round-trip verification."""

    backend_id = "echo-backend:v0.1"

    def execute(self, handoff: Mapping[str, Any]) -> BackendResponse:
        return BackendResponse(
            backend_id=self.backend_id,
            status="completed",
            payload={"echo": dict(handoff)},
        )

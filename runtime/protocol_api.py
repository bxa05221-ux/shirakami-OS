"""Generic Protocol invocation API boundary.

A Protocol remains the source artifact. This module exposes a small
parameterized invocation request without creating one endpoint per Protocol.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .protocol_registry import ProtocolRegistry, ProtocolRegistryError


class ProtocolAPIError(ProtocolRegistryError):
    """Raised when a Protocol invocation cannot be resolved."""


@dataclass(frozen=True)
class ProtocolRequest:
    """Parameterized request for invoking a registered Protocol."""

    protocol_id: str
    version: str | None
    input: Mapping[str, Any]


def build_protocol_request(
    registry: ProtocolRegistry,
    protocol_id: str,
    input_data: Mapping[str, Any] | None = None,
    version: str | None = None,
) -> ProtocolRequest:
    """Resolve an eligible Protocol and expose it as a Runtime parameter set."""
    try:
        entry = registry.select_current(protocol_id)
    except ProtocolRegistryError as exc:
        raise ProtocolAPIError(str(exc)) from exc

    artifact = entry.artifact
    artifact_version = getattr(artifact, "version", None)
    if isinstance(artifact, Mapping):
        artifact_version = artifact.get("version", artifact_version)

    resolved_version = version if version is not None else (
        str(artifact_version) if artifact_version is not None else None
    )
    return ProtocolRequest(
        protocol_id=entry.protocol_id,
        version=resolved_version,
        input=dict(input_data or {}),
    )

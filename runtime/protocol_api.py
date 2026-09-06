"""Generic Protocol invocation API boundary.

A Protocol remains the source artifact. This module exposes a small
parameterized invocation surface without creating one endpoint per Protocol.
"""

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .protocol_registry import ProtocolRegistry, ProtocolRegistryError
from .route_map import RouteMap


class ProtocolAPIError(ProtocolRegistryError):
    """Raised when a Protocol invocation cannot be resolved."""


@dataclass(frozen=True)
class ProtocolRequest:
    """Parameterized request for invoking a registered Protocol."""

    protocol_id: str
    version: str | None
    input: Mapping[str, Any]


def _request_from_entry(
    entry: Any,
    input_data: Mapping[str, Any] | None = None,
    version: str | None = None,
) -> ProtocolRequest:
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
    return _request_from_entry(entry, input_data=input_data, version=version)


def build_default_protocol_request(
    registry: ProtocolRegistry,
    input_data: Mapping[str, Any] | None = None,
    version: str | None = None,
) -> ProtocolRequest:
    """Resolve the mandatory OS default Protocol."""
    try:
        entry = registry.require_default()
    except ProtocolRegistryError as exc:
        raise ProtocolAPIError(str(exc)) from exc
    if entry.state == "archived":
        raise ProtocolAPIError("default protocol cannot be archived")
    return _request_from_entry(entry, input_data=input_data, version=version)


def invoke_protocol(
    request: ProtocolRequest,
    executor: Callable[[ProtocolRequest], Any],
) -> Any:
    """Invoke a resolved Protocol through an injected execution boundary.

    The API owns request resolution and transport-neutral dispatch only. The
    executor owns execution semantics and may be backed by any Runtime adapter
    or external application.
    """
    if not callable(executor):
        raise ProtocolAPIError("executor is required")
    return executor(request)


def invoke_and_record_route(
    request: ProtocolRequest,
    executor: Callable[[ProtocolRequest], Any],
    route_map: RouteMap,
) -> tuple[Any, RouteMap]:
    """Dispatch a Protocol request and record the observed destination.

    The executor remains responsible for execution semantics. Route recording
    only preserves the fact that the requested Protocol was traversed.
    """
    result = invoke_protocol(request, executor)
    return result, route_map.record_transition(request.protocol_id)

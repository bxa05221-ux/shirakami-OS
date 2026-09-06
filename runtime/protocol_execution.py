"""Generic Protocol execution boundary for the post-MVP Runtime layer."""

from collections.abc import Callable, Mapping
from typing import Any

from .evidence import capture_evidence
from .protocol_api import ProtocolRequest, invoke_protocol
from .route_map import RouteMap


def execute_protocol_request(
    request: ProtocolRequest,
    executor: Callable[[ProtocolRequest], Any],
    route_map: RouteMap,
) -> tuple[Any, RouteMap]:
    """Execute a resolved Protocol request and record the observed destination.

    Execution semantics remain owned by the injected executor. This boundary
    only connects the generic request surface to existing Runtime evidence and
    observable route state.
    """
    result = invoke_protocol(request, executor)
    if hasattr(result, "protocol_id"):
        protocol_id = result.protocol_id
    else:
        protocol_id = request.protocol_id

    evidence = None
    if hasattr(result, "transition"):
        evidence = capture_evidence(result)

    updated_route = route_map.record_transition(protocol_id)
    return {"result": result, "evidence": evidence}, updated_route

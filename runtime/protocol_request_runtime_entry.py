"""R0085 ProtocolRequest -> Runtime entry boundary.

Implementation-only bridge. It does not interpret Protocol semantics,
change Registry behavior, or claim autonomous execution.
"""

from typing import Any, Callable

from .protocol_api import ProtocolRequest, ProtocolAPIError


def execute_protocol_request(
    request: ProtocolRequest,
    executor: Callable[[ProtocolRequest], Any],
) -> Any:
    """Pass a resolved ProtocolRequest into an existing Runtime executor."""
    if not isinstance(request, ProtocolRequest):
        raise ProtocolAPIError("ProtocolRequest is required")
    if not callable(executor):
        raise ProtocolAPIError("executor is required")
    return executor(request)

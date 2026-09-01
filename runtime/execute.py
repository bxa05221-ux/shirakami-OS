"""Minimal Protocol -> MTM -> Runtime execution path."""

from typing import Any, Mapping

from .current_protocol import load_current_protocol
from .mtm_runtime import RuntimeProtocol, prepare_runtime_protocol
from .protocol_registry import ProtocolRegistry


def execute_current_protocol(
    path: str,
    registry: ProtocolRegistry,
    protocol_id: str,
    input_data: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    """Load, normalize, and execute the minimum Runtime path.

    The MVP Runtime records the protocol identity and input snapshot. It does
    not interpret protocol semantics or invoke an AI provider yet.
    """
    protocol = load_current_protocol(path, registry, protocol_id)
    runtime_protocol: RuntimeProtocol = prepare_runtime_protocol(protocol)
    return {
        "protocol_id": runtime_protocol.protocol_id,
        "version": runtime_protocol.version,
        "input": dict(input_data or {}),
        "status": "prepared",
    }

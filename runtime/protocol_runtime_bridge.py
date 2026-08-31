"""Minimal bridge from Protocol IR to the existing Runtime vertical slice."""

from dataclasses import dataclass
from typing import Any, Callable, Mapping

try:
    # Legacy runtime tests import modules as top-level names. Reuse that
    # module when available so Transition identity remains identical across
    # the bridge and test-provided protocol functions.
    from prototype import ExecutionResult, Runtime, Transition
except ImportError:
    from runtime.prototype import ExecutionResult, Runtime, Transition


@dataclass(frozen=True)
class ProtocolExecution:
    protocol_title: str
    protocol_version: str
    result: ExecutionResult


def execute_protocol(
    protocol_ir: dict[str, Any],
    transition: Callable[[Mapping[str, Any]], Transition],
    *,
    input_value: Any = None,
) -> ProtocolExecution:
    """Execute a loaded Protocol IR through the existing Runtime boundary.

    The bridge adapts the current β0.1 Runtime signature without introducing
    new protocol semantics.
    """
    matome = protocol_ir.get("matome", protocol_ir)
    if not isinstance(matome, dict):
        raise ValueError("protocol IR must contain an object-like matome")

    title = str(matome.get("title", ""))
    version = str(matome.get("version", ""))
    protocol_id = title or "anonymous.protocol"

    def runtime_protocol(context):
        return transition(context.input)

    runtime = Runtime()
    normalized_input = input_value if isinstance(input_value, Mapping) else {}
    result = runtime.execute(protocol_id, runtime_protocol, normalized_input)
    return ProtocolExecution(
        protocol_title=title,
        protocol_version=version,
        result=result,
    )

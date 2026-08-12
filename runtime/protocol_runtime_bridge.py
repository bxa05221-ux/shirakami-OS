"""Minimal bridge from Protocol IR to the existing Runtime vertical slice.

This module intentionally keeps the bridge small. It adapts the currently
supported Protocol IR into the callable transition interface already used by
Runtime, without introducing a new runtime architecture.
"""

from dataclasses import dataclass
from typing import Any, Callable

from runtime.runtime import Runtime, ExecutionResult


@dataclass(frozen=True)
class ProtocolExecution:
    protocol_title: str
    protocol_version: str
    result: ExecutionResult


def execute_protocol(
    protocol_ir: dict[str, Any],
    transition: Callable[[Any], Any],
    *,
    input_value: Any = None,
) -> ProtocolExecution:
    """Execute a loaded Protocol IR through the existing Runtime.

    The bridge deliberately does not invent protocol semantics. The supplied
    callable remains the concrete transition supported by the Runtime.
    """
    matome = protocol_ir.get("matome", protocol_ir)
    title = matome.get("title", "")
    version = str(matome.get("version", ""))

    runtime = Runtime()
    result = runtime.execute(transition, input_value)
    return ProtocolExecution(
        protocol_title=title,
        protocol_version=version,
        result=result,
    )

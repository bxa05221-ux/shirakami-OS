"""Explicit handoff from Activation to Runtime execution.

This boundary consumes an already-activated Protocol. It does not approve,
promote, or select a Protocol.
"""

from __future__ import annotations

from typing import Any, Mapping

try:
    from .activation import ActivationResult
    from .prototype import ExecutionResult, Protocol, Runtime
except ImportError:
    from activation import ActivationResult
    from prototype import ExecutionResult, Protocol, Runtime


class ActivationExecutionError(RuntimeError):
    """Raised when an activation result cannot enter Runtime execution."""


def execute_activated(
    activation: ActivationResult,
    runtime: Runtime,
    protocol: Protocol,
    input_data: Mapping[str, Any] | None = None,
) -> ExecutionResult:
    """Execute exactly the Protocol authorized by an activated result."""

    if activation.status != "activated":
        raise ActivationExecutionError(
            "Runtime execution requires an activated Protocol"
        )

    if not activation.protocol_id.strip():
        raise ActivationExecutionError("activated protocol_id is required")

    return runtime.execute(
        activation.protocol_id,
        protocol,
        input_data if input_data is not None else activation.context,
    )

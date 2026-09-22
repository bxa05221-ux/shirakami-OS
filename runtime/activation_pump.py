"""Minimal downstream release boundary for authorized Activations.

The Activation Pump releases an already-authorized ActivationResult. It does
not approve, promote, select, or create execution authority. Scheduling and
queue management are intentionally outside this implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
from uuid import uuid4

try:
    from .activation import ActivationResult
    from .prototype import ExecutionResult, Protocol, Runtime
except ImportError:
    from activation import ActivationResult
    from prototype import ExecutionResult, Protocol, Runtime


class ActivationPumpError(RuntimeError):
    """Raised when an activation cannot be released safely."""


@dataclass(frozen=True)
class PumpRelease:
    """Observable execution-control event created when an activation is released."""

    release_id: str
    protocol_id: str
    status: str
    context: Mapping[str, Any]


class ActivationPump:
    """Fail-closed release boundary for already-authorized Activations."""

    def release(self, activation: ActivationResult) -> PumpRelease:
        """Release an activation without changing its authority or identity."""

        if activation.status != "activated":
            raise ActivationPumpError(
                "pump release requires an activated Protocol"
            )

        if not isinstance(activation.protocol_id, str) or not activation.protocol_id.strip():
            raise ActivationPumpError("pump release requires a non-empty protocol_id")

        if not isinstance(activation.context, Mapping):
            raise ActivationPumpError("activation context must be a mapping")

        return PumpRelease(
            release_id=str(uuid4()),
            protocol_id=activation.protocol_id,
            status="released",
            context=dict(activation.context),
        )

    def execute(
        self,
        release: PumpRelease,
        runtime: Runtime,
        protocol: Protocol,
        input_data: Mapping[str, Any] | None = None,
    ) -> ExecutionResult:
        """Hand one released activation to Runtime without expanding its scope."""

        if release.status != "released":
            raise ActivationPumpError(
                "Runtime execution requires a released Pump event"
            )

        if not isinstance(release.protocol_id, str) or not release.protocol_id.strip():
            raise ActivationPumpError("released protocol_id is required")

        return runtime.execute(
            release.protocol_id,
            protocol,
            input_data if input_data is not None else release.context,
        )


def release_activation(activation: ActivationResult) -> PumpRelease:
    """Functional convenience wrapper around the Activation Pump boundary."""

    return ActivationPump().release(activation)


def execute_released(
    release: PumpRelease,
    runtime: Runtime,
    protocol: Protocol,
    input_data: Mapping[str, Any] | None = None,
) -> ExecutionResult:
    """Functional convenience wrapper for Runtime handoff."""

    return ActivationPump().execute(release, runtime, protocol, input_data)


__all__ = [
    "ActivationPump",
    "ActivationPumpError",
    "PumpRelease",
    "release_activation",
    "execute_released",
]

"""Observable execution cycle for an already-activated Protocol.

This composes Activation with the existing EvidenceDrivenRuntime. It does not
create approval or alter the Human Gate; it only consumes an activation result
and records the existing execution/verification/evidence flow.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping

try:
    from .activation import ActivationResult
    from .evolution_bridge import VerificationResult
    from .evolution_pipeline import EvidenceDrivenRuntime
    from .prototype import ExecutionResult, Transition
except ImportError:
    from activation import ActivationResult
    from evolution_bridge import VerificationResult
    from evolution_pipeline import EvidenceDrivenRuntime
    from prototype import ExecutionResult, Transition


class ActivatedCycleError(RuntimeError):
    """Raised when an activated Protocol cannot enter the observable cycle."""


def execute_activated_cycle(
    activation: ActivationResult,
    runtime: EvidenceDrivenRuntime,
    protocol: Callable[[Any], Transition],
    *,
    expected_transition_kind: str | None = None,
    input_data: Mapping[str, Any] | None = None,
) -> tuple[ExecutionResult, VerificationResult]:
    """Execute, verify, and retain Evidence for an activated Protocol."""

    if activation.status != "activated":
        raise ActivatedCycleError(
            "observable execution requires an activated Protocol"
        )
    if not activation.protocol_id.strip():
        raise ActivatedCycleError("activated protocol_id is required")

    execution = runtime.execute(
        protocol,
        activation.protocol_id,
        input_data if input_data is not None else activation.context,
    )
    verification = runtime.verify(
        execution,
        expected_transition_kind=expected_transition_kind,
        diff_ref=activation.protocol_id,
    )
    return execution, verification

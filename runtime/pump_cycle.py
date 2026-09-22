"""Bridge an Activation Pump release into the observable execution cycle.

The Pump only releases an already-authorized activation. This module consumes
that release and then enters the existing Runtime -> Verification -> Evidence
cycle. It does not create or modify authorization.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping

try:
    from .activated_cycle import ActivatedCycleError, execute_activated_cycle
    from .activation import ActivationResult
    from .activation_pump import PumpRelease
    from .evolution_bridge import VerificationResult
    from .evolution_pipeline import EvidenceDrivenRuntime
    from .prototype import ExecutionResult, Transition
except ImportError:
    from activated_cycle import ActivatedCycleError, execute_activated_cycle
    from activation import ActivationResult
    from activation_pump import PumpRelease
    from evolution_bridge import VerificationResult
    from evolution_pipeline import EvidenceDrivenRuntime
    from prototype import ExecutionResult, Transition


class PumpCycleError(RuntimeError):
    """Raised when a Pump release cannot enter the observable cycle."""


def execute_released_cycle(
    release: PumpRelease,
    runtime: EvidenceDrivenRuntime,
    protocol: Callable[[Any], Transition],
    *,
    expected_transition_kind: str | None = None,
    input_data: Mapping[str, Any] | None = None,
) -> tuple[ExecutionResult, VerificationResult]:
    """Execute, verify, and record Evidence for one Pump release."""

    if release.status != "released":
        raise PumpCycleError("observable cycle requires a released Pump event")

    if not isinstance(release.protocol_id, str) or not release.protocol_id.strip():
        raise PumpCycleError("released protocol_id is required")

    activation = ActivationResult(
        protocol_id=release.protocol_id,
        status="activated",
        context=release.context,
    )

    try:
        return execute_activated_cycle(
            activation=activation,
            runtime=runtime,
            protocol=protocol,
            expected_transition_kind=expected_transition_kind,
            input_data=input_data,
        )
    except ActivatedCycleError as exc:
        raise PumpCycleError(str(exc)) from exc


__all__ = ["PumpCycleError", "execute_released_cycle"]

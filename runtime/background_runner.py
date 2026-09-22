"""Minimal non-authoritative Background Runner boundary.

The Runner consumes a released Activation Pump event and maintains execution
context for a bounded sequence of observable cycles. It does not schedule,
approve, promote, select, or broaden authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping
from uuid import uuid4

try:
    from .activation_pump import PumpRelease
    from .evolution_bridge import VerificationResult
    from .evolution_pipeline import EvidenceDrivenRuntime
    from .pump_cycle import PumpCycleError, execute_released_cycle
    from .prototype import ExecutionResult, Transition
except ImportError:
    from activation_pump import PumpRelease
    from evolution_bridge import VerificationResult
    from evolution_pipeline import EvidenceDrivenRuntime
    from pump_cycle import PumpCycleError, execute_released_cycle
    from prototype import ExecutionResult, Transition


class BackgroundRunnerError(RuntimeError):
    """Raised when a released activation cannot enter Runner execution."""


@dataclass(frozen=True)
class RunnerExecution:
    """Observable execution-control event for one Runner iteration."""

    run_id: str
    iteration: int
    protocol_id: str
    status: str
    execution: ExecutionResult
    verification: VerificationResult


class BackgroundRunner:
    """Bounded execution-context holder with no governance authority."""

    def run(
        self,
        release: PumpRelease,
        runtime: EvidenceDrivenRuntime,
        protocol: Callable[[Any], Transition],
        *,
        iterations: int = 1,
        expected_transition_kind: str | None = None,
        input_data: Mapping[str, Any] | None = None,
    ) -> tuple[RunnerExecution, ...]:
        """Run a released activation for a bounded number of observable iterations."""

        if release.status != "released":
            raise BackgroundRunnerError(
                "Runner requires a released Pump event"
            )

        if not isinstance(release.protocol_id, str) or not release.protocol_id.strip():
            raise BackgroundRunnerError("Runner requires a non-empty protocol_id")

        if not isinstance(iterations, int) or iterations < 1:
            raise BackgroundRunnerError("iterations must be an integer >= 1")

        run_id = str(uuid4())
        results: list[RunnerExecution] = []

        for iteration in range(1, iterations + 1):
            try:
                execution, verification = execute_released_cycle(
                    release,
                    runtime,
                    protocol,
                    expected_transition_kind=expected_transition_kind,
                    input_data=input_data,
                )
            except PumpCycleError as exc:
                raise BackgroundRunnerError(str(exc)) from exc

            results.append(
                RunnerExecution(
                    run_id=run_id,
                    iteration=iteration,
                    protocol_id=release.protocol_id,
                    status="completed",
                    execution=execution,
                    verification=verification,
                )
            )

        return tuple(results)


__all__ = ["BackgroundRunner", "BackgroundRunnerError", "RunnerExecution"]

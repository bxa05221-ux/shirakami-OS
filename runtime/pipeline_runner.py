"""Explicit Approved Pipeline -> Background Runner -> Evidence boundary.

This adapter preserves pipeline identity and execution order while delegating
actual execution to the existing bounded Background Runner. It does not create
or expand authority and does not reinterpret Runner evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

try:
    from .activation_pump import ReleasedActivation
    from .background_runner import RunnerResult, run_released_activation
    from .evidence import EvidenceRecord
except ImportError:
    from activation_pump import ReleasedActivation
    from background_runner import RunnerResult, run_released_activation
    from evidence import EvidenceRecord


class PipelineRunnerError(ValueError):
    """Raised when the pipeline-to-runner boundary cannot fail safely."""


@dataclass(frozen=True)
class PipelineRunnerEvidence:
    """Immutable per-item evidence with explicit pipeline provenance."""

    pipeline_identity: str
    execution_order: int
    activation_identity: str
    protocol_identity: str
    approval_identity: str
    run_identity: str
    evidence: EvidenceRecord


@dataclass(frozen=True)
class PipelineRunnerResult:
    """Observed execution result for one approved pipeline."""

    pipeline_identity: str
    items: tuple[PipelineRunnerEvidence, ...]
    runner_results: tuple[RunnerResult, ...]
    stopped: bool = False


def run_approved_pipeline_on_runner(
    *,
    pipeline_identity: str,
    activations: Iterable[ReleasedActivation],
    iteration_budget: int,
    execute: Callable[[ReleasedActivation, int], bool],
    verify: Callable[[ReleasedActivation, int], bool],
) -> PipelineRunnerResult:
    """Run an explicit Activation sequence through the existing Runner.

    Order and identities are carried as context. They never become authority.
    The first Runner verification mismatch stops subsequent pipeline items.
    """

    if not pipeline_identity.strip():
        raise PipelineRunnerError("pipeline identity is required")

    items = tuple(activations)
    observed: list[PipelineRunnerEvidence] = []
    runner_results: list[RunnerResult] = []

    for order, activation in enumerate(items, start=1):
        _validate_activation(activation)

        # Run identity is explicit, deterministic pipeline context.
        run_id = f"{pipeline_identity}:run:{order}"

        try:
            result = run_released_activation(
                activation=activation,
                iteration_budget=iteration_budget,
                run_id=run_id,
                execute=execute,
                verify=verify,
            )
        except Exception as exc:
            # The existing Runner owns failure semantics. The pipeline stops
            # rather than inventing a replacement Evidence record.
            raise PipelineRunnerError("runner execution failed") from exc

        runner_results.append(result)
        observed.extend(
            _to_pipeline_evidence(
                pipeline_identity=pipeline_identity,
                execution_order=order,
                result=result,
            )
        )

        if result.state.value != "COMPLETED":
            return PipelineRunnerResult(
                pipeline_identity=pipeline_identity,
                items=tuple(observed),
                runner_results=tuple(runner_results),
                stopped=True,
            )

    return PipelineRunnerResult(
        pipeline_identity=pipeline_identity,
        items=tuple(observed),
        runner_results=tuple(runner_results),
        stopped=False,
    )


def _validate_activation(activation: ReleasedActivation) -> None:
    if not isinstance(activation, ReleasedActivation):
        raise PipelineRunnerError("released activation is required")
    if not activation.activation_id.strip():
        raise PipelineRunnerError("activation identity is required")
    if not activation.protocol_id.strip():
        raise PipelineRunnerError("protocol identity is required")
    if not activation.approval_reviewer.strip():
        raise PipelineRunnerError("approval identity is required")


def _to_pipeline_evidence(
    *,
    pipeline_identity: str,
    execution_order: int,
    result: RunnerResult,
) -> tuple[PipelineRunnerEvidence, ...]:
    records: list[PipelineRunnerEvidence] = []

    for evidence in result.evidence:
        transition_data = dict(
            evidence_record_data(evidence)
        )
        transition_data["pipeline_identity"] = pipeline_identity
        transition_data["execution_order"] = execution_order

        canonical = EvidenceRecord(
            protocol_id=evidence.protocol_identity,
            status="observed",
            transition_kind=f"runner:{evidence.event}",
            transition_data=transition_data,
            signals=(f"runner:{evidence.event}",),
        )
        records.append(
            PipelineRunnerEvidence(
                pipeline_identity=pipeline_identity,
                execution_order=execution_order,
                activation_identity=evidence.activation_identity,
                protocol_identity=evidence.protocol_identity,
                approval_identity=evidence.approval_identity,
                run_identity=evidence.run_identity,
                evidence=canonical,
            )
        )

    return tuple(records)


def evidence_record_data(evidence) -> dict[str, object]:
    return {
        "event": evidence.event,
        "protocol_identity": evidence.protocol_identity,
        "activation_identity": evidence.activation_identity,
        "approval_identity": evidence.approval_identity,
        "run_identity": evidence.run_identity,
        "iteration": evidence.iteration,
        "runner_state": evidence.runner_state,
    }

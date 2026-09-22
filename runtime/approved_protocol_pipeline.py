"""Bounded pipeline for already-approved Runtime Activations.

The Pipeline is an execution coordinator, not an authority source. It accepts
only explicit ReleasedActivation inputs and preserves their identity/order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

try:
    from .activation_pump import ReleasedActivation
except ImportError:
    from activation_pump import ReleasedActivation


class PipelineError(ValueError):
    pass


@dataclass(frozen=True)
class PipelineItemResult:
    execution_order: int
    activation_identity: str
    protocol_identity: str
    approval_identity: str
    result: object


@dataclass(frozen=True)
class PipelineResult:
    pipeline_identity: str
    items: tuple[PipelineItemResult, ...]
    stopped: bool = False


def run_approved_pipeline(
    *,
    pipeline_identity: str,
    activations: Iterable[ReleasedActivation],
    execute: Callable[[ReleasedActivation, int], object],
) -> PipelineResult:
    """Execute explicitly ordered released activations; stop on first failure."""
    if not pipeline_identity:
        raise PipelineError("pipeline identity is required")

    items = tuple(activations)
    results: list[PipelineItemResult] = []

    for index, activation in enumerate(items, start=1):
        if not isinstance(activation, ReleasedActivation):
            raise PipelineError("pipeline accepts ReleasedActivation only")
        if not activation.activation_identity:
            raise PipelineError("missing activation identity")
        if not activation.protocol_identity:
            raise PipelineError("missing protocol identity")
        if not activation.approval_identity:
            raise PipelineError("missing approval identity")

        try:
            value = execute(activation, index)
        except Exception as exc:
            return PipelineResult(
                pipeline_identity=pipeline_identity,
                items=tuple(results + [
                    PipelineItemResult(
                        execution_order=index,
                        activation_identity=activation.activation_identity,
                        protocol_identity=activation.protocol_identity,
                        approval_identity=activation.approval_identity,
                        result=exc,
                    )
                ]),
                stopped=True,
            )

        results.append(
            PipelineItemResult(
                execution_order=index,
                activation_identity=activation.activation_identity,
                protocol_identity=activation.protocol_identity,
                approval_identity=activation.approval_identity,
                result=value,
            )
        )

    return PipelineResult(
        pipeline_identity=pipeline_identity,
        items=tuple(results),
        stopped=False,
    )

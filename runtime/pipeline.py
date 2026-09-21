"""Protocol-owned Pipeline plan boundary.

A Pipeline is derived from a selected Protocol artifact and execution context.
It is not a separate registry or semantic authority in v0.1.
"""

from dataclasses import dataclass
from typing import Mapping, Any


class PipelineError(ValueError):
    """Raised when a Pipeline plan cannot be resolved."""


@dataclass(frozen=True)
class PipelineStep:
    phase: str
    action: str


@dataclass(frozen=True)
class PipelinePlan:
    protocol_id: str
    version: str
    steps: tuple[PipelineStep, ...]
    context: Mapping[str, Any]


def build_pipeline_plan(
    protocol: Any,
    context: Mapping[str, Any] | None = None,
) -> PipelinePlan:
    """Derive an executable Pipeline plan from an already selected Protocol.

    This function does not select the Protocol, choose a backend, or mutate the
    Protocol artifact.
    """
    protocol_id = getattr(protocol, "protocol_id", None)
    version = getattr(protocol, "version", None)
    pipeline = getattr(protocol, "pipeline", None)

    if not isinstance(protocol_id, str) or not protocol_id:
        raise PipelineError("selected Protocol must have protocol_id")
    if not isinstance(version, str) or not version:
        raise PipelineError("selected Protocol must have version")
    if not isinstance(pipeline, (list, tuple)) or not pipeline:
        raise PipelineError("selected Protocol must have a non-empty pipeline")

    steps: list[PipelineStep] = []
    for item in pipeline:
        if not isinstance(item, Mapping):
            raise PipelineError("pipeline step must be a mapping")
        phase = item.get("phase")
        action = item.get("action")
        if not isinstance(phase, str) or not phase:
            raise PipelineError("pipeline step requires phase")
        if not isinstance(action, str) or not action:
            raise PipelineError("pipeline step requires action")
        steps.append(PipelineStep(phase=phase, action=action))

    return PipelinePlan(
        protocol_id=protocol_id,
        version=version,
        steps=tuple(steps),
        context=dict(context or {}),
    )

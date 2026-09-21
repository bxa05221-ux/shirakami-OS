"""Explicit execution trace for Protocol -> Pipeline -> Adapter runs.

The trace aggregates observable step results without deciding whether outputs are
true, verified, or authoritative. Semantic verification remains outside this
execution layer.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from runtime.adapter import PipelineAdapter, PipelineAdapterRequest, PipelineAdapterResult
from runtime.pipeline import PipelinePlan
from runtime.protocol_api import ProtocolRequest


@dataclass(frozen=True)
class PipelineExecutionTrace:
    protocol_id: str
    version: str
    context: Mapping[str, Any]
    steps: tuple[PipelineAdapterResult, ...]

    @property
    def backends(self) -> tuple[str, ...]:
        return tuple(step.backend for step in self.steps)

    @property
    def completed(self) -> bool:
        """Return whether all planned steps returned an execution result.

        Completion describes execution flow only. It does not assert that an
        output is true, verified, or authoritative.
        """
        return bool(self.steps)


def execute_pipeline_plan(
    request: ProtocolRequest,
    plan: PipelinePlan,
    adapter: PipelineAdapter,
) -> PipelineExecutionTrace:
    """Execute an already selected plan through one explicit adapter.

    This function does not select Protocols, Pipelines, or AI backends and does
    not promote adapter output into verified Evidence.
    """
    if request.protocol_id != plan.protocol_id:
        raise ValueError("request and plan protocol_id must match")
    if request.version != plan.version:
        raise ValueError("request and plan version must match")

    results: list[PipelineAdapterResult] = []
    for step in plan.steps:
        results.append(
            adapter.execute(
                PipelineAdapterRequest(
                    protocol_id=plan.protocol_id,
                    version=plan.version,
                    phase=step.phase,
                    action=step.action,
                    input=request.input,
                    context=plan.context,
                )
            )
        )

    return PipelineExecutionTrace(
        protocol_id=plan.protocol_id,
        version=plan.version,
        context=plan.context,
        steps=tuple(results),
    )

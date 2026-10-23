"""ThreadRPG-specific independent observation, conference, and matome flow."""

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .adapter import PipelineAdapter, PipelineAdapterRequest, PipelineAdapterResult


class ThreadRPGExecutionError(ValueError):
    """Raised when ThreadRPG execution inputs are invalid."""


@dataclass(frozen=True)
class ThreadRPGExecutionResult:
    protocol_id: str
    version: str
    perspective_ids: tuple[str, ...]
    observations: tuple[PipelineAdapterResult, ...]
    conference: PipelineAdapterResult
    matome: PipelineAdapterResult

    @property
    def trace(self) -> tuple[tuple[str, PipelineAdapterResult], ...]:
        return (
            tuple(
                (f"observation:{pid}", result)
                for pid, result in zip(self.perspective_ids, self.observations)
            )
            + (("conference", self.conference), ("matome", self.matome))
        )


def execute_thread_rpg(
    *,
    task: Mapping[str, Any],
    perspectives: Sequence[Mapping[str, Any]],
    adapter: PipelineAdapter,
    context: Mapping[str, Any] | None = None,
    protocol_id: str = "thread_rpg",
    version: str = "0.1",
) -> ThreadRPGExecutionResult:
    """Run independent observations, then conference, then matome.

    This function records adapter outputs only. It does not update Landscape
    or make human-authoritative decisions.
    """
    if not isinstance(task, Mapping):
        raise ThreadRPGExecutionError("task must be a mapping")
    if not callable(getattr(adapter, "execute", None)):
        raise ThreadRPGExecutionError("adapter must provide execute(request)")
    if not protocol_id or not version:
        raise ThreadRPGExecutionError("protocol_id and version are required")
    if isinstance(perspectives, (str, bytes)) or len(perspectives) < 2:
        raise ThreadRPGExecutionError("at least two perspectives are required")

    ids: list[str] = []
    for perspective in perspectives:
        if not isinstance(perspective, Mapping):
            raise ThreadRPGExecutionError("each perspective must be a mapping")
        pid = perspective.get("id")
        if not isinstance(pid, str) or not pid.strip():
            raise ThreadRPGExecutionError("each perspective requires a non-empty id")
        if pid in ids:
            raise ThreadRPGExecutionError(f"duplicate perspective id: {pid}")
        ids.append(pid)

    shared_context = dict(context or {})
    observations: list[PipelineAdapterResult] = []

    # Each perspective gets a separate adapter invocation and receives no
    # other perspective's output.
    for perspective in perspectives:
        pid = str(perspective["id"])
        result = adapter.execute(
            PipelineAdapterRequest(
                protocol_id=protocol_id,
                version=version,
                phase="independent_observation",
                action="observe_landscape",
                input={
                    "task": dict(task),
                    "perspective": dict(perspective),
                },
                context={**shared_context, "perspective_id": pid},
                previous_outputs=(),
            )
        )
        observations.append(result)

    observation_payload = [
        {
            "perspective_id": pid,
            "output": result.output,
            "backend": result.backend,
            "evidence": dict(result.evidence),
        }
        for pid, result in zip(ids, observations)
    ]

    conference = adapter.execute(
        PipelineAdapterRequest(
            protocol_id=protocol_id,
            version=version,
            phase="conference",
            action="compare_observations_preserving_differences",
            input={
                "task": dict(task),
                "observations": observation_payload,
                "instruction": (
                    "Compare viewpoints. Preserve disagreements, contradictions, "
                    "and unresolved questions; do not force consensus."
                ),
            },
            context=shared_context,
            previous_outputs=tuple(observations),
        )
    )

    matome = adapter.execute(
        PipelineAdapterRequest(
            protocol_id=protocol_id,
            version=version,
            phase="matome",
            action="organize_findings_and_unresolved_questions",
            input={
                "task": dict(task),
                "observations": observation_payload,
                "conference": {
                    "output": conference.output,
                    "backend": conference.backend,
                    "evidence": dict(conference.evidence),
                },
                "instruction": (
                    "Summarize findings while retaining distinct viewpoints, "
                    "contradictions, and unresolved questions. Do not make a "
                    "human decision or update Landscape."
                ),
            },
            context=shared_context,
            previous_outputs=tuple(observations) + (conference,),
        )
    )

    return ThreadRPGExecutionResult(
        protocol_id=protocol_id,
        version=version,
        perspective_ids=tuple(ids),
        observations=tuple(observations),
        conference=conference,
        matome=matome,
    )

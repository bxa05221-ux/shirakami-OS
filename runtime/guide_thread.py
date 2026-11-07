"""Data-only Guide Thread boundaries.

Guide Thread records Protocol-derived work and may expose a Runtime candidate,
but it neither selects that candidate nor executes it implicitly.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from .adapter import PipelineAdapter, PipelineAdapterRequest, PipelineAdapterResult
from .pipeline import PipelinePlan
from .protocol_api import ProtocolRequest


class GuideThreadError(ValueError):
    """Raised when a Guide Thread boundary is used without an explicit choice."""


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class GuideThreadRequest:
    """One Protocol Pipeline step copied into the Guide Thread boundary."""

    protocol: str
    version: str
    phase: str
    action: str
    input: Mapping[str, Any]
    context: Mapping[str, Any]

    def __post_init__(self) -> None:
        for field in ("protocol", "version", "phase", "action"):
            if not isinstance(getattr(self, field), str) or not getattr(self, field):
                raise GuideThreadError(f"{field} is required")
        object.__setattr__(self, "input", _freeze(self.input))
        object.__setattr__(self, "context", _freeze(self.context))


@dataclass(frozen=True)
class GuideThreadRuntimeCandidate:
    """An immutable proposed Runtime input; it has no execution authority."""

    request: GuideThreadRequest
    authority: str = "not_inferred"
    executable: bool = False


@dataclass(frozen=True)
class SelectedGuideThreadRuntimeCandidate:
    """A candidate explicitly selected by the caller for the existing Runtime."""

    candidate: GuideThreadRuntimeCandidate


def build_guide_thread_requests(
    request: ProtocolRequest,
    plan: PipelinePlan,
) -> tuple[GuideThreadRequest, ...]:
    """Copy a selected Protocol's steps without selecting or running anything."""
    if request.protocol_id != plan.protocol_id:
        raise GuideThreadError("Protocol request and Pipeline plan must match")
    if request.version is not None and request.version != plan.version:
        raise GuideThreadError("Protocol request and Pipeline version must match")
    return tuple(
        GuideThreadRequest(
            protocol=plan.protocol_id,
            version=plan.version,
            phase=step.phase,
            action=step.action,
            input=request.input,
            context=plan.context,
        )
        for step in plan.steps
    )


def propose_runtime_candidate(request: GuideThreadRequest) -> GuideThreadRuntimeCandidate:
    """Expose a possible next Runtime input without executing or authorizing it."""
    return GuideThreadRuntimeCandidate(request=request)


def select_runtime_candidate(
    candidate: GuideThreadRuntimeCandidate,
) -> SelectedGuideThreadRuntimeCandidate:
    """Make the required explicit caller selection visible at the boundary."""
    if not isinstance(candidate, GuideThreadRuntimeCandidate):
        raise GuideThreadError("Guide Thread Runtime candidate is required")
    return SelectedGuideThreadRuntimeCandidate(candidate=candidate)


def execute_selected_runtime_candidate(
    selected: SelectedGuideThreadRuntimeCandidate,
    adapter: PipelineAdapter,
) -> PipelineAdapterResult:
    """Pass only an explicitly selected candidate to the existing Adapter entry."""
    if not isinstance(selected, SelectedGuideThreadRuntimeCandidate):
        raise GuideThreadError("explicitly selected Guide Thread candidate is required")
    request = selected.candidate.request
    return adapter.execute(
        PipelineAdapterRequest(
            protocol_id=request.protocol,
            version=request.version,
            phase=request.phase,
            action=request.action,
            input=request.input,
            context=request.context,
        )
    )

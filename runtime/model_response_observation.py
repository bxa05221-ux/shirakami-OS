"""Observation-only model-response to pending-next-turn boundary."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from .adapter import PipelineAdapterResult
from .evidence import EvidenceRecord
from .guide_thread import GuideThreadRuntimeCandidate


def _frozen_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class PendingNextTurn:
    """A non-executable next-turn candidate retained only as observed data."""

    evidence: EvidenceRecord
    candidate: GuideThreadRuntimeCandidate
    auto_execute: bool = False
    authority: str = "not_inferred"


def observe_model_response(
    result: PipelineAdapterResult,
    candidate: GuideThreadRuntimeCandidate,
) -> PendingNextTurn:
    """Record opaque model output and return a non-running next-turn candidate.

    The returned value deliberately has no adapter or execution callback.  A
    later caller must make a separate explicit selection before it can cross
    the Guide Thread -> Runtime boundary.
    """
    if not isinstance(result, PipelineAdapterResult):
        raise TypeError("result must be a PipelineAdapterResult")
    if not isinstance(candidate, GuideThreadRuntimeCandidate):
        raise TypeError("candidate must be a GuideThreadRuntimeCandidate")
    request = candidate.request
    evidence = EvidenceRecord(
        protocol_id=request.protocol,
        status="observed",
        transition_kind="model.response.observed",
        transition_data=_frozen_mapping(
            {
                "backend": result.backend,
                "output": result.output,
                "adapter_evidence": dict(result.evidence),
                "phase": request.phase,
                "action": request.action,
                "authority": "not_inferred",
            }
        ),
        signals=("model.response.observed",),
        confidence="observed",
    )
    return PendingNextTurn(evidence=evidence, candidate=candidate)

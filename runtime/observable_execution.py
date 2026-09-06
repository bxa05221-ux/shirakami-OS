"""Inspectable Runtime execution result boundary for β0.1."""

from dataclasses import dataclass
from typing import Any, Mapping

from .adapter import adapt_landscape_observation
from .evidence import EvidenceRecord
from .landscape import LandscapeState
from .landscape_execution import execute_on_landscape
from .prototype import Protocol, Runtime


@dataclass(frozen=True)
class ObservableExecutionResult:
    """One inspectable execution view: before, evidence, after, re-observation."""

    before_state: Mapping[str, Any]
    evidence: EvidenceRecord
    after_state: Mapping[str, Any]
    observation: Mapping[str, Any]


def execute_observably(
    state: LandscapeState,
    runtime: Runtime,
    protocol_id: str,
    protocol: Protocol,
    input_data: Mapping[str, Any] | None = None,
) -> ObservableExecutionResult:
    """Execute through the existing Runtime loop and expose its observable path."""
    before_state = state.snapshot()
    evidence = execute_on_landscape(state, runtime, protocol_id, protocol, input_data)
    after_state = state.snapshot()
    observation = adapt_landscape_observation(state)
    return ObservableExecutionResult(before_state, evidence, after_state, observation)

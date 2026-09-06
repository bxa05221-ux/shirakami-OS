"""Observable result boundary for a single Runtime execution."""

from dataclasses import dataclass
from typing import Any, Mapping

from .adapter import adapt_landscape_observation
from .evidence import EvidenceRecord
from .landscape import LandscapeState
from .landscape_execution import execute_on_landscape
from .prototype import Protocol, Runtime


@dataclass(frozen=True)
class ObservableExecutionResult:
    """Inspectable before/after representation of one Runtime execution."""

    before: Mapping[str, Any]
    evidence: EvidenceRecord
    after: Mapping[str, Any]
    observation: Mapping[str, Any]


def execute_observable(
    state: LandscapeState,
    runtime: Runtime,
    protocol_id: str,
    protocol: Protocol,
    input_data: Mapping[str, Any] | None = None,
) -> ObservableExecutionResult:
    """Execute one Protocol and expose the resulting observable state."""
    before = state.snapshot()
    evidence = execute_on_landscape(state, runtime, protocol_id, protocol, input_data)
    after = state.snapshot()
    observation = adapt_landscape_observation(state)
    return ObservableExecutionResult(
        before=before,
        evidence=evidence,
        after=after,
        observation=observation,
    )

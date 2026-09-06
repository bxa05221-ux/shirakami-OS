"""Minimal external Landscape -> Runtime -> Evidence -> Landscape loop."""

from typing import Any, Mapping

from .evidence import capture_evidence
from .landscape import LandscapeState
from .prototype import ExecutionResult, Protocol, Runtime


def execute_on_landscape(
    state: LandscapeState,
    protocol_id: str,
    protocol: Protocol,
    input_data: Mapping[str, Any] | None = None,
    runtime: Runtime | None = None,
) -> ExecutionResult:
    """Execute one Protocol against an existing Landscape and project Evidence."""
    result = (runtime or Runtime()).execute(protocol_id, protocol, input_data)
    evidence = capture_evidence(result)
    state.apply_evidence(evidence)
    return result

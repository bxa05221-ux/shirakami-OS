"""Minimal Landscape execution loop boundary for Runtime β0.1."""

from typing import Any, Mapping

from .evidence import EvidenceRecord, capture_evidence
from .landscape import LandscapeState
from .prototype import Protocol, Runtime


def execute_on_landscape(
    state: LandscapeState,
    runtime: Runtime,
    protocol_id: str,
    protocol: Protocol,
    input_data: Mapping[str, Any] | None = None,
) -> EvidenceRecord:
    """Execute one Protocol and apply its observed transition to the state."""
    result = runtime.execute(protocol_id, protocol, input_data)
    evidence = capture_evidence(result)
    state.apply_evidence(evidence)
    return evidence

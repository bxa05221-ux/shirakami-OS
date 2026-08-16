"""Complete β0.1 vertical slice from Matome Protocol to Landscape state.

Matome YAML -> ProtocolIR -> Runtime -> ExecutionResult -> Evidence -> Landscape.
This module only composes existing boundaries; it does not introduce protocol
semantics.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from evidence import EvidenceRecord, capture_evidence
from landscape import LandscapeState
from protocol_bridge import protocol_from_ir
from protocol_loader import ProtocolIR, load_matome
from prototype import ExecutionResult, Runtime


@dataclass(frozen=True)
class VerticalSliceResult:
    """Inspectable result of one complete β0.1 execution path."""

    protocol: ProtocolIR
    execution: ExecutionResult
    evidence: EvidenceRecord
    landscape: Mapping[str, Any]


def execute_matome(path: str | Path, input_value: Mapping[str, Any] | None = None) -> VerticalSliceResult:
    """Load, execute, capture evidence, and project one Matome Protocol."""

    protocol = load_matome(path)
    runtime = Runtime()
    runtime_protocol = protocol_from_ir(protocol)
    normalized_input = input_value if isinstance(input_value, Mapping) else {}

    execution = runtime.execute(
        protocol.protocol_id,
        runtime_protocol,
        normalized_input,
    )
    evidence = capture_evidence(execution)

    landscape = LandscapeState.empty()
    landscape.apply_evidence(evidence)

    return VerticalSliceResult(
        protocol=protocol,
        execution=execution,
        evidence=evidence,
        landscape=landscape.snapshot(),
    )

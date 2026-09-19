"""Canonical ProtocolIR -> Runtime -> Evidence execution boundary.

This module preserves the existing prepared-snapshot path in ``execute.py``
and exposes the complete execution/evidence path as an explicit operation.
It does not introduce protocol semantics or provider-specific behavior.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

try:
    from .current_protocol import load_current_protocol
    from .evidence import EvidenceRecord, capture_evidence
    from .protocol_bridge import protocol_from_ir
    from .protocol_registry import ProtocolRegistry
    from .protocol_loader import ProtocolIR
    from .prototype import ExecutionResult, Runtime
except ImportError:
    from current_protocol import load_current_protocol
    from evidence import EvidenceRecord, capture_evidence
    from protocol_bridge import protocol_from_ir
    from protocol_registry import ProtocolRegistry
    from protocol_loader import ProtocolIR
    from prototype import ExecutionResult, Runtime


@dataclass(frozen=True)
class ExecutionEvidenceResult:
    """Inspectable result of one Registry-selected execution."""

    protocol: ProtocolIR
    execution: ExecutionResult
    evidence: EvidenceRecord


def execute_current_protocol_with_evidence(
    path: str | Path,
    registry: ProtocolRegistry,
    protocol_id: str,
    input_data: Mapping[str, Any] | None = None,
) -> ExecutionEvidenceResult:
    """Execute a current Protocol and capture immutable EvidenceRecord."""
    protocol = load_current_protocol(path, registry, protocol_id)
    runtime_protocol = protocol_from_ir(protocol)
    execution = Runtime().execute(
        protocol.protocol_id,
        runtime_protocol,
        input_data,
    )
    evidence = capture_evidence(execution)
    return ExecutionEvidenceResult(
        protocol=protocol,
        execution=execution,
        evidence=evidence,
    )

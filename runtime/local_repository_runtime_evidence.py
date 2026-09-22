"""Local Repository -> Runtime -> Evidence vertical integration boundary.

This module composes existing boundaries without introducing protocol semantics:
Local Repository storage -> ProtocolIR -> Runtime -> Evidence -> Landscape.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .evidence import EvidenceRecord, capture_evidence
from .landscape import LandscapeState
from .local_repository_loader import LocalRepositoryProtocolLoader
from .protocol_bridge import protocol_from_ir
from .protocol_loader import ProtocolIR
from .prototype import ExecutionResult, Runtime


@dataclass(frozen=True)
class LocalRepositoryExecutionResult:
    """Inspectable result of one local protocol execution."""

    protocol: ProtocolIR
    execution: ExecutionResult
    evidence: EvidenceRecord
    landscape: Mapping[str, Any]


def execute_local_repository_protocol(
    root: str | Path,
    protocol_path: str,
    landscape: Mapping[str, Any] | None = None,
    input_data: Mapping[str, Any] | None = None,
) -> LocalRepositoryExecutionResult:
    """Load, execute, capture Evidence, and apply it to current Landscape.

    The function composes existing boundaries only. It does not select a
    protocol, interpret domain-specific semantics, or choose an AI backend.
    """
    protocol = LocalRepositoryProtocolLoader(root).load(protocol_path)
    current_landscape = LandscapeState.from_snapshot(landscape or {})
    runtime_protocol = protocol_from_ir(protocol)

    execution = Runtime().execute(
        protocol.protocol_id,
        runtime_protocol,
        input_data,
    )
    evidence = capture_evidence(execution)
    current_landscape.apply_evidence(evidence)

    return LocalRepositoryExecutionResult(
        protocol=protocol,
        execution=execution,
        evidence=evidence,
        landscape=current_landscape.snapshot(),
    )

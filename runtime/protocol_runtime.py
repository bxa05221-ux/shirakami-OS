"""Bridge declared Protocol IR to the existing minimal Runtime and Evidence boundary."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .evidence import EvidenceRecord, capture_evidence
from .protocol_ir import ProtocolIR
from .prototype import ExecutionResult, Runtime, Transition


@dataclass(frozen=True)
class ProtocolExecution:
    result: ExecutionResult
    evidence: EvidenceRecord


def execute_protocol_ir(
    protocol_ir: ProtocolIR,
    protocol: Callable[[Any], Transition],
    *,
    runtime: Runtime | None = None,
) -> ProtocolExecution:
    """Execute only the transition already declared in Protocol IR."""
    active_runtime = runtime or Runtime()
    result = active_runtime.execute(
        protocol_ir.protocol_id,
        protocol,
        {
            "context_id": protocol_ir.context_id,
            "parent_landscape_ref": protocol_ir.parent_landscape_ref,
            "transition_kind": protocol_ir.transition_kind,
            "transition_data": protocol_ir.transition_data,
        },
    )
    return ProtocolExecution(result=result, evidence=capture_evidence(result))

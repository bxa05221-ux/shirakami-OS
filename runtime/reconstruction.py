"""End-to-end trace reconstruction for the Shirakami MVP.

This module links the AIwitness simulation record to the human decision,
operation result, and any resulting Evidence references. It does not execute
an operation or infer facts that are not explicitly supplied.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .aiwitness import WitnessRecord
from .operation import HumanDecision, OperationResult


@dataclass(frozen=True)
class ReconstructionTrace:
    """A verifiable chain from input Evidence to resulting Evidence."""

    witness_id: str
    prompt_id: str
    protocol_id: str
    simulation_id: str
    decision_id: str
    operation_id: str
    decision_status: str
    operation_status: str
    reality_changed: bool
    input_evidence_refs: tuple[str, ...]
    resulting_evidence_refs: tuple[str, ...]
    context_version: str | None
    uncertainty: tuple[str, ...]


def reconstruct_trace(
    *,
    witness: WitnessRecord,
    decision: HumanDecision,
    operation: OperationResult,
    resulting_evidence_refs: tuple[str, ...] = (),
) -> ReconstructionTrace:
    """Assemble an explicit trace without inventing missing evidence."""
    if witness.simulation_id != decision.simulation_id:
        raise ValueError("witness and decision do not match")
    if witness.simulation_id != operation.simulation_id:
        raise ValueError("witness and operation do not match")
    if decision.decision_id != operation.decision_id:
        raise ValueError("decision and operation do not match")

    return ReconstructionTrace(
        witness_id=witness.witness_id,
        prompt_id=witness.prompt_id,
        protocol_id=witness.protocol_id,
        simulation_id=witness.simulation_id,
        decision_id=decision.decision_id,
        operation_id=operation.operation_id,
        decision_status=decision.status,
        operation_status=operation.status,
        reality_changed=operation.reality_changed,
        input_evidence_refs=tuple(witness.evidence_refs),
        resulting_evidence_refs=tuple(resulting_evidence_refs),
        context_version=witness.context_version,
        uncertainty=tuple(witness.uncertainty),
    )


def trace_as_evidence(trace: ReconstructionTrace) -> Mapping[str, Any]:
    """Serialize the reconstruction chain as an Evidence-shaped record."""
    return {
        "kind": "reconstruction_trace",
        "witness_id": trace.witness_id,
        "prompt_id": trace.prompt_id,
        "protocol_id": trace.protocol_id,
        "simulation_id": trace.simulation_id,
        "decision_id": trace.decision_id,
        "operation_id": trace.operation_id,
        "decision_status": trace.decision_status,
        "operation_status": trace.operation_status,
        "reality_changed": trace.reality_changed,
        "input_evidence_refs": trace.input_evidence_refs,
        "resulting_evidence_refs": trace.resulting_evidence_refs,
        "context_version": trace.context_version,
        "uncertainty": trace.uncertainty,
    }

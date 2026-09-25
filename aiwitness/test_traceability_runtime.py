"""Integration tests for the runtime-to-AIwitness provenance chain."""

from __future__ import annotations

from typing import Any

from evolution_bridge import ContextSnapshot
from evolution_pipeline import EvidenceDrivenRuntime
from prototype import Transition
from api import ShirakamiAPI
from aiwitness.traceability import validate_traceability


def _protocol(_: Any) -> Transition:
    return Transition(kind="traceability.example", data={"changed": True})


def _context() -> ContextSnapshot:
    return ContextSnapshot(
        protocol_id="traceability.example",
        landscape={"topic": "provenance"},
        metadata={"source": "traceability-test"},
    )


def test_runtime_execution_forms_machine_checkable_provenance_chain() -> None:
    api = ShirakamiAPI(EvidenceDrivenRuntime())
    api.observe({}, _context())
    api.analyze("traceability.example", protocol_exists=True)

    result = api.execute(_protocol, "traceability.example", {}, handoff_id="SH-HO-20260925-001", project="Shirakami Project", objective="Validate runtime provenance", protocol_ids=("traceability.example",), verification_scope=("runtime provenance",))
    execution = api.get_execution(result["execution_id"])
    trace = api.get_trace(result["trace_id"])
    witness = api.get_witness(result["trace_id"])

    assert execution is not None and trace is not None and witness is not None
    record = validate_traceability(execution=execution, trace=trace, witness=witness, evidence_ids=result["evidence_ids"])
    assert record.handoff_id == "SH-HO-20260925-001"
    assert record.execution_id == result["execution_id"]
    assert record.trace_id == result["trace_id"]
    assert record.witness_id == witness["witness_id"]
    assert record.evidence_ids == tuple(result["evidence_ids"])
    assert record.verification_status == "pending"
    assert record.commit is None


def test_runtime_provenance_chain_remains_aligned_after_verification() -> None:
    api = ShirakamiAPI(EvidenceDrivenRuntime())
    api.observe({}, _context())
    api.analyze("traceability.example", protocol_exists=True)
    result = api.execute(_protocol, "traceability.example", {}, handoff_id="SH-HO-20260925-001", project="Shirakami Project", objective="Verify provenance revision", protocol_ids=("traceability.example",), verification_scope=("verification",))

    checked = api.verify_execution(result["execution_id"], expected_transition_kind="traceability.example")
    assert checked is not None and checked.status == "pass"
    execution = api.get_execution(result["execution_id"])
    trace = api.get_trace(result["trace_id"])
    witness = api.get_witness(result["trace_id"])
    history = api.get_witness_history(result["trace_id"])

    assert execution is not None and trace is not None and witness is not None
    assert len(history) == 2
    assert history[0]["witness_id"] != history[1]["witness_id"]
    record = validate_traceability(execution=execution, trace=trace, witness=witness, evidence_ids=result["evidence_ids"])
    assert record.verification_status == "pass"
    assert trace["verification_status"] == witness["verification_status"] == "pass"
    assert trace["verification_observed"]["transition_kind"] == "traceability.example"
    assert witness["witness_id"] == history[-1]["witness_id"]

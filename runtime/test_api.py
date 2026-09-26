"""Tests for the UI for AI API boundary α0.1."""

from __future__ import annotations

from typing import Any

from evolution_bridge import ContextSnapshot
from evolution_pipeline import EvidenceDrivenRuntime
from prototype import Transition
from api import ShirakamiAPI


def _protocol(_: Any) -> Transition:
    return Transition(kind="api.example", data={"changed": True})


def _api() -> ShirakamiAPI:
    return ShirakamiAPI(EvidenceDrivenRuntime())


def _context() -> ContextSnapshot:
    return ContextSnapshot(
        protocol_id="api.example",
        landscape={"topic": "ui-for-ai"},
        metadata={"source": "test"},
    )


def _ready_api() -> ShirakamiAPI:
    api = _api()
    api.observe({"signal": "execute"}, _context())
    api.analyze("api.example", protocol_exists=True)
    return api


def test_observe_exposes_evidence_boundary() -> None:
    api = _api()
    result = api.observe({"signal": "hello"}, _context())
    assert result["state"] == "EVIDENCE"
    assert any(item["signals"] == ["CONTEXT_SNAPSHOT"] for item in result["evidence"])


def test_human_gate_requires_explicit_authorization() -> None:
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)

    api = _api()
    api.observe({}, _context())
    api.analyze("api.new", protocol_exists=False, diff_ref="diff-1")

    denied = api.approve(approved=True, reviewer="human")
    assert denied["accepted"] is False
    assert "authorization" in denied["reason"]

    accepted = api.approve(approved=True, reviewer="human", human_authorized=True)
    assert accepted["accepted"] is True
    assert accepted["state"] == "READY"


def test_execute_and_query_are_provider_neutral() -> None:
    api = _ready_api()
    result = api.execute(_protocol, "api.example", {"input": 1}, handoff_id="SH-HO-API-001")
    assert result["status"] == "completed"
    assert result["transition"]["kind"] == "api.example"
    evidence = api.query_evidence(protocol_id="api.example")
    assert evidence
    assert all(item["protocol_id"] == "api.example" for item in evidence)


def test_mismatch_is_queryable() -> None:
    api = _ready_api()
    execution = api.runtime.execute(_protocol, "api.example", {})
    api.runtime.loop.dispatch("verify", {"status": execution.status})
    api.verify(execution, expected_transition_kind="different")
    mismatch = api.query_evidence(signal="MISMATCH")
    assert mismatch
    assert mismatch[-1]["signals"] == ["MISMATCH"]


def test_execution_handle_is_stable_and_verifiable() -> None:
    api = _ready_api()
    result = api.execute(_protocol, "api.example", {}, handoff_id="SH-HO-API-002")
    execution_id = result["execution_id"]
    handle = api.get_execution(execution_id)
    assert handle is not None
    assert handle["execution_id"] == execution_id
    assert handle["status"] == "completed"
    assert api.get_execution("missing-execution-id") is None
    verification = api.verify_execution(execution_id, expected_transition_kind="api.example")
    assert verification is not None
    assert verification.status == "pass"


def test_execution_handle_mismatch_becomes_evidence() -> None:
    api = _ready_api()
    result = api.execute(_protocol, "api.example", {}, handoff_id="SH-HO-API-003")
    verification = api.verify_execution(result["execution_id"], expected_transition_kind="different", diff_ref="diff-1")
    assert verification is not None
    assert verification.status == "mismatch"
    assert api.query_evidence(signal="MISMATCH")


def test_execution_preserves_trace_metadata_without_authority() -> None:
    api = _ready_api()
    result = api.execute(_protocol, "api.example", {}, handoff_id="SH-HO-20260925-001", trace_id="TRACE-001", evidence_ids=("AGENT-COORDINATION-001",), project="Shirakami Project", objective="API provenance", protocol_ids=("api.example",), verification_scope=("runtime handle",))
    assert result["handoff_id"] == "SH-HO-20260925-001"
    assert result["trace_id"] == "TRACE-001"
    assert result["evidence_ids"] == ["AGENT-COORDINATION-001"]
    assert result["execution_authorized"] is False
    assert result["publish_authorized"] is False
    assert result["merge_authorized"] is False
    assert result["human_gate_required"] is True

    stored = api.get_execution(result["execution_id"])
    assert stored is not None
    assert stored["handoff_id"] == "SH-HO-20260925-001"
    assert stored["trace_id"] == "TRACE-001"
    assert stored["evidence_ids"] == ["AGENT-COORDINATION-001"]
    assert stored["project"] == "Shirakami Project"
    assert stored["objective"] == "API provenance"
    assert stored["protocol_ids"] == ["api.example"]
    assert stored["verification_scope"] == ["runtime handle"]


def test_execution_creates_and_verifies_evidence_trace() -> None:
    api = _ready_api()
    result = api.execute(_protocol, "api.example", {}, handoff_id="SH-HO-20260925-001", trace_id="TRACE-001", evidence_ids=("AGENT-COORDINATION-001",), project="Shirakami Project", objective="Execution trace", protocol_ids=("api.example",), verification_scope=("runtime handle",))
    trace = api.get_trace("TRACE-001")
    assert trace is not None
    assert trace["execution_id"] == result["execution_id"]
    assert trace["handoff_id"] == "SH-HO-20260925-001"
    assert trace["evidence_ids"] == ["AGENT-COORDINATION-001"]
    assert trace["verification_status"] == "pending"
    assert trace["execution_authorized"] is False
    verification = api.verify_execution(result["execution_id"], expected_transition_kind="api.example")
    assert verification is not None
    assert verification.status == "pass"
    verified_trace = api.get_trace("TRACE-001")
    assert verified_trace is not None
    assert verified_trace["verification_status"] == "pass"
    assert verified_trace["verification_observed"]["transition_kind"] == "api.example"
    assert verified_trace["execution_authorized"] is False


def test_execution_generates_trace_when_trace_id_is_absent() -> None:
    api = _ready_api()
    result = api.execute(_protocol, "api.example", {}, handoff_id="SH-HO-API-004")
    trace_id = result["trace_id"]
    assert trace_id.startswith("TRACE-")
    trace = api.get_trace(trace_id)
    assert trace is not None
    assert trace["execution_id"] == result["execution_id"]
    assert api.get_execution(result["execution_id"])["trace_id"] == trace_id


def test_generated_evidence_id_is_shared_by_handle_and_trace() -> None:
    api = _ready_api()
    result = api.execute(_protocol, "api.example", {}, handoff_id="SH-HO-API-005")
    stored = api.get_execution(result["execution_id"])
    trace = api.get_trace(result["trace_id"])
    assert stored is not None
    assert trace is not None
    assert stored["evidence_ids"] == trace["evidence_ids"]
    assert stored["evidence_ids"]


def test_execution_records_aiwitness_observation() -> None:
    api = _api()
    def protocol(_: Any) -> Transition:
        return Transition(kind="api.witness", data={"changed": True})
    api.observe({}, ContextSnapshot(protocol_id="api.witness", landscape={}, metadata={}))
    api.analyze("api.witness", protocol_exists=True)
    result = api.execute(protocol, "api.witness", {"input": "test"}, handoff_id="SH-HO-API-006", project="Shirakami", objective="record witness", protocol_ids=("api.witness",), verification_scope=("execution",))
    witness = api.get_witness(result["trace_id"])
    assert witness is not None
    assert witness["trace_id"] == result["trace_id"]
    assert witness["execution_id"] == result["execution_id"]
    assert witness["handoff_id"] == result["handoff_id"]
    assert witness["evidence_ids"] == result["evidence_ids"]
    assert witness["execution_authorized"] is False
    assert witness["publish_authorized"] is False
    assert witness["merge_authorized"] is False
    assert witness["human_gate_required"] is True


def test_unknown_aiwitness_fails_closed() -> None:
    api = _api()
    assert api.get_witness("TRACE-UNKNOWN") is None


def test_execution_witness_has_stable_identity() -> None:
    api = _api()
    def protocol(_: Any) -> Transition:
        return Transition(kind="api.witness.identity", data={"changed": True})
    api.observe({}, ContextSnapshot(protocol_id="api.witness.identity", landscape={}, metadata={}))
    api.analyze("api.witness.identity", protocol_exists=True)
    result = api.execute(protocol, "api.witness.identity", handoff_id="SH-HO-API-007", project="Shirakami", objective="verify witness identity", protocol_ids=("api.witness.identity",))
    witness = api.get_witness(result["trace_id"])
    assert witness is not None
    assert witness["witness_id"].startswith("WITNESS-")


def test_witness_refreshes_after_verify() -> None:
    api = _api()
    def protocol(_: Any) -> Transition:
        return Transition(kind="api.witness.refresh", data={"changed": True})
    api.observe({}, ContextSnapshot(protocol_id="api.witness.refresh", landscape={}, metadata={}))
    api.analyze("api.witness.refresh", protocol_exists=True)
    result = api.execute(protocol, "api.witness.refresh", handoff_id="SH-HO-API-008", project="Shirakami", objective="refresh witness", protocol_ids=("api.witness.refresh",))
    before = api.get_witness(result["trace_id"])
    assert before is not None
    assert before["verification_status"] == "pending"
    checked = api.verify_execution(result["execution_id"], expected_transition_kind="api.witness.refresh")
    assert checked is not None
    assert checked.status == "pass"
    after = api.get_witness(result["trace_id"])
    assert after is not None
    assert after["verification_status"] == "pass"
    assert after["trace_id"] == before["trace_id"]
    assert after["execution_id"] == before["execution_id"]
    assert after["evidence_ids"] == before["evidence_ids"]
    assert after["witness_id"] != before["witness_id"]


def test_real_model_output_is_bound_to_evidence_trace_and_aiwitness() -> None:
    api = _ready_api()
    result = api.execute(
        _protocol,
        "api.example",
        {"text": "external model observation"},
        handoff_id="SH-HO-REALMODEL-001",
        project="Shirakami",
        objective="real model provenance",
        protocol_ids=("api.example",),
        ai_adapter=lambda prompt, protocol_id: {
            "output": "provider-neutral-model-response",
            "prompt": prompt,
            "protocol_id": protocol_id,
        },
    )

    assert result["model_output"]["output"] == "provider-neutral-model-response"
    evidence = api.get_evidence(result["evidence_ids"][0])
    assert evidence is not None
    assert evidence["model_output"]["output"] == "provider-neutral-model-response"

    trace = api.get_trace(result["trace_id"])
    assert trace is not None
    assert result["evidence_ids"] == trace["evidence_ids"]

    witness = api.get_witness(result["trace_id"])
    assert witness is not None
    assert witness["evidence_ids"] == trace["evidence_ids"]
    assert witness["execution_id"] == result["execution_id"]
    assert witness["execution_authorized"] is False
    assert witness["publish_authorized"] is False
    assert witness["merge_authorized"] is False
    assert witness["human_gate_required"] is True


def test_model_output_changes_evidence_id() -> None:
    outputs = [
        {"output": "response-a"},
        {"output": "response-b"},
    ]
    results = [
        _ready_api().execute(_protocol, "api.example", {"text": "same observation"}, handoff_id="SH-HO-EVIDENCE-ID", ai_adapter=lambda _p, _i, value=value: value)
        for value in outputs
    ]
    assert results[0]["evidence_ids"][0] != results[1]["evidence_ids"][0]


def test_same_model_output_is_deterministically_bound_to_evidence_id() -> None:
    def run_once() -> str:
        api = _ready_api()
        result = api.execute(
            _protocol,
            "api.example",
            {"text": "same observation"},
            handoff_id="SH-HO-EVIDENCE-DETERMINISTIC",
            ai_adapter=lambda _p, _i: {"output": "same-response"},
        )
        return result["evidence_ids"][0]

    assert run_once() == run_once()


def test_serialized_model_output_matches_retrieved_evidence() -> None:
    api = _ready_api()
    model_output = {"output": "serialization-check", "provider": "fixture"}
    result = api.execute(
        _protocol,
        "api.example",
        {"text": "serialization"},
        handoff_id="SH-HO-EVIDENCE-SERIALIZATION",
        ai_adapter=lambda _p, _i: model_output,
    )
    evidence = api.get_evidence(result["evidence_ids"][0])
    assert evidence is not None
    assert result["model_output"] == evidence["model_output"] == model_output

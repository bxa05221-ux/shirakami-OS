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


def test_observe_exposes_evidence_boundary() -> None:
    api = _api()
    result = api.observe({"signal": "hello"}, _context())

    assert result["state"] == "EVIDENCE"
    assert any(
        item["signals"] == ["CONTEXT_SNAPSHOT"]
        for item in result["evidence"]
    )


def test_human_gate_requires_explicit_authorization() -> None:
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)

    # Existing protocols do not require Human Review in R0100.
    # Move the API into a candidate flow to exercise the gate.
    api = _api()
    api.observe({}, _context())
    api.analyze("api.new", protocol_exists=False, diff_ref="diff-1")

    denied = api.approve(approved=True, reviewer="human")
    assert denied["accepted"] is False
    assert "authorization" in denied["reason"]

    accepted = api.approve(
        approved=True,
        reviewer="human",
        human_authorized=True,
    )
    assert accepted["accepted"] is True
    assert accepted["state"] == "READY"


def test_execute_and_query_are_provider_neutral() -> None:
    api = _api()
    api.observe({"signal": "execute"}, _context())
    api.analyze("api.example", protocol_exists=True)

    result = api.execute(_protocol, "api.example", {"input": 1})

    assert result["status"] == "completed"
    assert result["transition"]["kind"] == "api.example"

    evidence = api.query_evidence(protocol_id="api.example")
    assert evidence
    assert all(item["protocol_id"] == "api.example" for item in evidence)


def test_mismatch_is_queryable() -> None:
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)
    execution = api.runtime.execute("api.example", _protocol, {})
    api.runtime.loop.dispatch("verify", {"status": execution.status})
    api.verify(execution, expected_transition_kind="different")

    mismatch = api.query_evidence(signal="MISMATCH")
    assert mismatch
    assert mismatch[-1]["signals"] == ["MISMATCH"]


def test_execution_handle_is_stable_and_verifiable() -> None:
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)
    result = api.execute(_protocol, "api.example", {})

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
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)
    result = api.execute(_protocol, "api.example", {})

    verification = api.verify_execution(result["execution_id"], expected_transition_kind="different", diff_ref="diff-1")
    assert verification is not None
    assert verification.status == "mismatch"
    assert api.query_evidence(signal="MISMATCH")


def test_execution_handle_is_stable_and_verifiable() -> None:
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)
    result = api.execute(_protocol, "api.example", {})
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
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)
    result = api.execute(_protocol, "api.example", {})
    verification = api.verify_execution(result["execution_id"], expected_transition_kind="different", diff_ref="diff-1")
    assert verification is not None
    assert verification.status == "mismatch"
    assert api.query_evidence(signal="MISMATCH")


def test_execution_preserves_trace_metadata_without_authority() -> None:
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)

    result = api.execute(
        _protocol,
        "api.example",
        {},
        handoff_id="SH-HO-20260925-001",
        trace_id="TRACE-001",
        evidence_ids=("AGENT-COORDINATION-001",),
        project="Shirakami Project",
        objective="API provenance",
        protocol_ids=("api.example",),
        verification_scope=("runtime handle",),
    )

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
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)

    result = api.execute(
        _protocol,
        "api.example",
        {},
        handoff_id="SH-HO-20260925-001",
        trace_id="TRACE-001",
        evidence_ids=("AGENT-COORDINATION-001",),
        project="Shirakami Project",
        objective="Execution trace",
        protocol_ids=("api.example",),
        verification_scope=("runtime handle",),
    )

    trace = api.get_trace("TRACE-001")
    assert trace is not None
    assert trace["execution_id"] == result["execution_id"]
    assert trace["handoff_id"] == "SH-HO-20260925-001"
    assert trace["evidence_ids"] == ["AGENT-COORDINATION-001"]
    assert trace["verification_status"] == "pending"
    assert trace["execution_authorized"] is False
    assert trace["publish_authorized"] is False
    assert trace["merge_authorized"] is False
    assert trace["human_gate_required"] is True

    verification = api.verify_execution(
        result["execution_id"],
        expected_transition_kind="api.example",
    )
    assert verification is not None
    assert verification.status == "pass"

    verified_trace = api.get_trace("TRACE-001")
    assert verified_trace is not None
    assert verified_trace["verification_status"] == "pass"
    assert verified_trace["verification_observed"]["transition_kind"] == "api.example"
    assert verified_trace["execution_authorized"] is False


def test_execution_generates_trace_when_trace_id_is_absent() -> None:
    api = _api()
    api.observe({}, _context())
    api.analyze("api.example", protocol_exists=True)

    result = api.execute(_protocol, "api.example", {})
    trace_id = result["trace_id"]

    assert trace_id.startswith("TRACE-")
    trace = api.get_trace(trace_id)
    assert trace is not None
    assert trace["execution_id"] == result["execution_id"]
    assert api.get_execution(result["execution_id"])["trace_id"] == trace_id

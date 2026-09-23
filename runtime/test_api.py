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
    assert all(item["evidence_id"] for item in result["evidence"])


def test_observe_returns_semantic_handoff_with_stable_evidence_identity() -> None:
    api = _api()
    result = api.observe({"signal": "hello"}, _context())

    handoff = result["semantic_handoff"]
    assert handoff["protocol_id"] == "api.example"
    assert handoff["runtime_state"] == "EVIDENCE"
    assert handoff["landscape"] == {"topic": "ui-for-ai"}
    assert handoff["metadata"] == {"source": "test"}
    assert handoff["observation_id"]

    evidence_ids = tuple(item["evidence_id"] for item in result["evidence"])
    assert handoff["evidence_ids"] == evidence_ids
    assert "approval" not in handoff
    assert "human_gate_result" not in handoff
    assert "execution_authorization" not in handoff
    assert "scope_expansion" not in handoff
    assert "candidate_promotion" not in handoff
    assert "provider_authority" not in handoff


def test_observe_creates_distinct_observation_identity() -> None:
    api = _api()
    first = api.observe({}, _context())["semantic_handoff"]["observation_id"]
    second = api.observe({}, _context())["semantic_handoff"]["observation_id"]
    assert first != second


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
    assert all(item["evidence_id"] for item in evidence)


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
    assert mismatch[-1]["evidence_id"]


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

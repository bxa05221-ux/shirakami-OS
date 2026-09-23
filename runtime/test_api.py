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
    assert any(item["signals"] == ["CONTEXT_SNAPSHOT"] for item in result["evidence"])


def test_observe_handoff_references_new_evidence_by_stable_id() -> None:
    api = _api()
    result = api.observe({"signal": "hello"}, _context())

    handoff = result["semantic_handoff"]
    evidence_ids = set(handoff["evidence_ids"])
    assert handoff["observation_id"]
    assert evidence_ids
    assert evidence_ids.issubset({item["evidence_id"] for item in result["evidence"]})
    assert all(item["evidence_id"] for item in result["evidence"])
    assert "approval" not in handoff
    assert "human_gate_result" not in handoff
    assert "execution_authorization" not in handoff


def test_observe_handoff_preserves_stable_identity_for_equivalent_evidence() -> None:
    api = _api()
    first = api.observe({"signal": "same"}, _context())
    second = api.observe({"signal": "same"}, _context())

    first_ids = set(first["semantic_handoff"]["evidence_ids"])
    second_ids = set(second["semantic_handoff"]["evidence_ids"])
    assert first_ids
    assert second_ids
    assert first_ids == second_ids


def test_observe_handoff_only_references_evidence_created_by_that_observation() -> None:
    api = _api()
    first = api.observe({"signal": "first"}, _context())
    second = api.observe({"signal": "second"}, _context())

    first_ids = set(first["semantic_handoff"]["evidence_ids"])
    second_ids = set(second["semantic_handoff"]["evidence_ids"])
    assert first_ids
    assert second_ids
    assert first_ids.isdisjoint(second_ids)


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

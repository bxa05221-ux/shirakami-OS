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

    assert result["status"] == "executed"
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

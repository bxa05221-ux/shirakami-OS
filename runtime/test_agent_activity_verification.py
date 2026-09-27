"""Tests for external Agent Activity verification."""

from runtime.agent_activity import ingest_agent_activity
from runtime.agent_activity_trace import AgentActivityTraceAdapter
from runtime.agent_activity_verification import (
    AgentActivityTraceVerifier,
    AgentActivityVerifier,
)
from runtime.trace import ExecutionTraceStore


def test_verification_is_separate_from_activity_claim() -> None:
    activity = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
    )

    verification = AgentActivityVerifier().verify(
        activity,
        method="repository_state_check",
        verified=True,
        observed={"target_exists": True},
    )

    assert verification.activity_id == activity.activity_id
    assert verification.status == "verified"
    assert verification.method == "repository_state_check"


def test_verification_updates_trace_without_granting_authority() -> None:
    traces = ExecutionTraceStore()
    adapter = AgentActivityTraceAdapter(traces)
    verifier = AgentActivityTraceVerifier(traces)

    activity = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
    )
    link = adapter.ingest(activity)

    verification = AgentActivityVerifier().verify(
        activity,
        method="repository_state_check",
        verified=True,
        observed={"target_exists": True},
    )
    trace = verifier.attach(link.trace_id, verification)

    assert trace is not None
    assert trace.verification_status == "verified"
    assert trace.verification_observed["verification"]["method"] == "repository_state_check"
    assert trace.execution_authorized is False
    assert trace.publish_authorized is False
    assert trace.merge_authorized is False
    assert trace.human_gate_required is True

"""Tests for the external Agent Activity trace bridge."""

from runtime.agent_activity import ingest_agent_activity
from runtime.agent_activity_trace import AgentActivityTraceAdapter
from runtime.trace import ExecutionTraceStore


def test_external_activity_creates_pending_trace_without_evidence() -> None:
    traces = ExecutionTraceStore()
    adapter = AgentActivityTraceAdapter(traces)

    activity = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
    )

    link = adapter.ingest(
        activity,
        project="bxa05221-ux/shirakami-OS",
        objective="review operation",
    )

    trace = traces.get(link.trace_id)

    assert trace is not None
    assert trace.execution_id == link.execution_id
    assert trace.handoff_id == link.handoff_id
    assert trace.evidence_ids == ()
    assert trace.verification_status == "pending"
    assert trace.verification_observed["activity_id"] == activity.activity_id
    assert trace.verification_observed["actor_type"] == "external_agent"
    assert trace.verification_observed["evidence_registered"] is False
    assert trace.execution_authorized is False
    assert trace.publish_authorized is False
    assert trace.merge_authorized is False
    assert trace.human_gate_required is True


def test_external_activity_trace_preserves_self_reported_boundary() -> None:
    traces = ExecutionTraceStore()
    adapter = AgentActivityTraceAdapter(traces)

    activity = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-2",
        source="github-copilot-cli",
        operation_type="search",
        target="ExecutionTrace",
        self_reported=True,
    )

    link = adapter.ingest(activity)
    trace = traces.get(link.trace_id)

    assert trace is not None
    assert trace.verification_observed["self_reported"] is True
    assert trace.verification_observed["external_verification_status"] == "unverified"

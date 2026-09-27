"""Tests for Activity -> Evidence -> Trace -> AIwitness closure."""

from runtime.agent_activity import ingest_agent_activity
from runtime.agent_activity_evidence_closure import AgentActivityEvidenceCloser
from runtime.agent_activity_trace import AgentActivityTraceAdapter
from runtime.agent_activity_verification import AgentActivityVerifier
from runtime.evidence_store import EvidenceStore
from runtime.trace import ExecutionTraceStore


def test_verified_activity_closes_into_trace_and_witness() -> None:
    activity = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
        result="read",
    )
    traces = ExecutionTraceStore()
    link = AgentActivityTraceAdapter(traces).ingest(
        activity,
        handoff_id="HANDOFF-review-1",
        project="bxa05221-ux/shirakami-OS",
        objective="record Copilot review activity",
    )
    verification = AgentActivityVerifier().verify(
        activity,
        method="repository_state_check",
        verified=True,
        observed={"target_exists": True},
    )

    closer = AgentActivityEvidenceCloser(traces, EvidenceStore())
    closure = closer.close(
        activity,
        verification,
        trace_id=link.trace_id,
        human_gate_confirmed=True,
    )

    trace = traces.get(link.trace_id)
    assert trace is not None
    assert closure.promotion.evidence_id in trace.evidence_ids
    assert closure.witness.trace_id == trace.trace_id
    assert closure.witness.evidence_ids == trace.evidence_ids
    assert closure.witness.verification_observed["evidence_registered"] is True
    assert closure.witness.execution_authorized is False
    assert closure.witness.publish_authorized is False
    assert closure.witness.merge_authorized is False
    assert closure.witness.human_gate_required is True

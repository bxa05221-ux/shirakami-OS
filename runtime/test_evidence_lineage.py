from __future__ import annotations

import pytest

from runtime.agent_activity import ingest_agent_activity
from runtime.agent_activity_trace import AgentActivityTraceAdapter
from runtime.evidence_lineage import EvidenceLineageBoundary
from runtime.trace import ExecutionTraceStore


def test_activity_and_runtime_evidence_share_one_trace_lineage() -> None:
    activity = ingest_agent_activity(
        agent_id="github-copilot-cli",
        session_id="session-1",
        source="github-copilot-cli-hook",
        operation_type="tool_call",
        target="README.md",
        input={"tool_name": "read_file"},
        self_reported=False,
    )
    traces = ExecutionTraceStore()
    link = AgentActivityTraceAdapter(traces).ingest(
        activity,
        handoff_id="HANDOFF-1",
        project="shirakami",
        objective="lineage",
    )
    trace = traces.get(link.trace_id)
    assert trace is not None

    lineage = EvidenceLineageBoundary().from_trace(
        trace,
        activity_id=activity.activity_id,
        sources=("agent_activity", "runtime"),
    )

    assert lineage.trace_id == link.trace_id
    assert lineage.execution_id == link.execution_id
    assert lineage.activity_id == activity.activity_id
    assert lineage.evidence_ids == ()
    assert lineage.sources == ("agent_activity", "runtime")


def test_lineage_rejects_authority_and_mismatched_activity() -> None:
    activity = ingest_agent_activity(
        agent_id="github-copilot-cli",
        source="github-copilot-cli-hook",
        operation_type="tool_call",
        self_reported=False,
    )
    traces = ExecutionTraceStore()
    link = AgentActivityTraceAdapter(traces).ingest(activity)
    trace = traces.get(link.trace_id)
    assert trace is not None

    boundary = EvidenceLineageBoundary()
    with pytest.raises(ValueError, match="activity_id does not match"):
        boundary.from_trace(trace, activity_id="other")

    with pytest.raises(ValueError, match="lineage cannot grant authority"):
        from runtime.evidence_lineage import EvidenceLineage
        EvidenceLineage(
            trace_id="t",
            execution_id="e",
            handoff_id=None,
            activity_id=None,
            evidence_ids=(),
            sources=("runtime",),
            execution_authorized=True,
        )


def test_require_evidence_is_exact() -> None:
    activity = ingest_agent_activity(
        agent_id="agent",
        source="test",
        operation_type="tool_call",
    )
    traces = ExecutionTraceStore()
    link = AgentActivityTraceAdapter(traces).ingest(activity)
    trace = traces.get(link.trace_id)
    assert trace is not None

    boundary = EvidenceLineageBoundary()
    lineage = boundary.from_trace(trace, sources=("runtime",))
    with pytest.raises(ValueError, match="not linked"):
        boundary.require_evidence(lineage, "missing-evidence")

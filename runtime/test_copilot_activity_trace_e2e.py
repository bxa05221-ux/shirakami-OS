"""End-to-end test for captured Copilot JSONL through Shirakami boundaries."""

from __future__ import annotations

import json

from runtime.agent_activity_evidence_closure import AgentActivityEvidenceCloser
from runtime.agent_activity_ingestor import AgentActivityIngestor
from runtime.agent_activity_trace import AgentActivityTraceAdapter
from runtime.agent_activity_verification import AgentActivityVerifier
from runtime.evidence_store import EvidenceStore
from runtime.trace import ExecutionTraceStore


def test_copilot_jsonl_reaches_trace_and_aiwitness_without_authority() -> None:
    line = json.dumps(
        {
            "agent_id": "github-copilot-cli",
            "session_id": "session-e2e",
            "source": "github-copilot-cli-hook",
            "operation_type": "tool_call",
            "target": "README.md",
            "input": {"tool_name": "cat", "tool_input": {"type": "string", "length": 9}},
            "result": {"result": {"type": "string", "length": 128}},
            "timestamp": "2026-09-26T00:00:00+00:00",
            "provenance": {"hook_event": "postToolUse"},
            "self_reported": False,
        }
    )

    activity = AgentActivityIngestor().ingest_lines([line])[0]
    traces = ExecutionTraceStore()
    link = AgentActivityTraceAdapter(traces).ingest(
        activity,
        handoff_id="HANDOFF-copilot-e2e",
        project="bxa05221-ux/shirakami-OS",
        objective="verify captured external activity boundary",
    )

    pending = traces.get(link.trace_id)
    assert pending is not None
    assert pending.verification_status == "pending"
    assert pending.evidence_ids == ()
    assert pending.execution_authorized is False
    assert pending.publish_authorized is False
    assert pending.merge_authorized is False
    assert pending.human_gate_required is True

    verification = AgentActivityVerifier().verify(
        activity,
        method="captured_jsonl_fixture_check",
        verified=True,
        observed={"jsonl_record_present": True, "target": "README.md"},
        uncertainty="fixture-level verification; not proof of the underlying external operation",
    )

    closure = AgentActivityEvidenceCloser(traces, EvidenceStore()).close(
        activity,
        verification,
        trace_id=link.trace_id,
        human_gate_confirmed=True,
    )

    trace = traces.get(link.trace_id)
    assert trace is not None
    assert trace.verification_status == "pass"
    assert trace.verification_uncertainty == verification.uncertainty
    assert closure.promotion.evidence_id in trace.evidence_ids
    assert closure.witness.trace_id == trace.trace_id
    assert closure.witness.evidence_ids == trace.evidence_ids
    assert closure.witness.execution_authorized is False
    assert closure.witness.publish_authorized is False
    assert closure.witness.merge_authorized is False
    assert closure.witness.human_gate_required is True

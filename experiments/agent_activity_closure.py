"""Concrete external-Agent activity closure harness.

This harness consumes an externally supplied activity record, verifies it using an
explicit verification result, and closes it through Evidence -> Trace -> AIwitness.
It deliberately does not execute the claimed external operation.
"""

from __future__ import annotations

import argparse
import json

from runtime.agent_activity import ingest_agent_activity
from runtime.agent_activity_evidence_closure import AgentActivityEvidenceCloser
from runtime.agent_activity_trace import AgentActivityTraceAdapter
from runtime.agent_activity_verification import AgentActivityVerifier
from runtime.evidence_store import EvidenceStore
from runtime.trace import ExecutionTraceStore


def close_activity(payload: dict) -> None:
    activity = ingest_agent_activity(
        agent_id=payload.get("agent_id"),
        session_id=payload.get("session_id"),
        source=payload["source"],
        operation_type=payload["operation_type"],
        target=payload.get("target"),
        input=payload.get("input"),
        result=payload.get("result"),
        timestamp=payload.get("timestamp"),
        provenance=payload.get("provenance", {}),
        self_reported=payload.get("self_reported", True),
    )

    traces = ExecutionTraceStore()
    link = AgentActivityTraceAdapter(traces).ingest(
        activity,
        handoff_id=payload.get("handoff_id"),
        project=payload.get("project"),
        objective=payload.get("objective"),
    )

    verification = AgentActivityVerifier().verify(
        activity,
        method=payload["verification_method"],
        verified=True,
        observed=payload.get("verification_observed", {}),
        uncertainty=payload.get("verification_uncertainty", ""),
    )

    closure = AgentActivityEvidenceCloser(
        traces,
        EvidenceStore(),
    ).close(
        activity,
        verification,
        trace_id=link.trace_id,
        human_gate_confirmed=payload.get("human_gate_confirmed", False),
    )

    trace = traces.get(link.trace_id)
    assert trace is not None
    assert closure.promotion.evidence_id in trace.evidence_ids

    print(json.dumps({
        "activity_id": activity.activity_id,
        "evidence_id": closure.promotion.evidence_id,
        "trace_id": closure.trace_id,
        "witness_id": closure.witness.witness_id,
        "verification_status": closure.witness.verification_status,
        "execution_authorized": closure.witness.execution_authorized,
        "publish_authorized": closure.witness.publish_authorized,
        "merge_authorized": closure.witness.merge_authorized,
        "human_gate_required": closure.witness.human_gate_required,
    }, ensure_ascii=False, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--activity-json", required=True)
    args = parser.parse_args()
    close_activity(json.loads(args.activity_json))


if __name__ == "__main__":
    main()

from __future__ import annotations

import pytest

from runtime.semantic_handoff import SemanticHandoff
from runtime.trace import ExecutionTrace


def _trace() -> ExecutionTrace:
    return ExecutionTrace(
        trace_id="TRACE-001",
        execution_id="EXEC-001",
        handoff_id="HANDOFF-001",
        evidence_ids=("EVIDENCE-001",),
        project="Shirakami",
        objective="lineage",
        protocol_ids=("protocol.example",),
        verification_scope=("execution",),
        verification_status="pass",
        verification_observed={"activity_id": "ACTIVITY-001"},
    )


def test_semantic_handoff_preserves_lineage_ids() -> None:
    handoff = SemanticHandoff.from_trace(_trace())

    assert handoff.handoff_id == "HANDOFF-001"
    assert handoff.trace_id == "TRACE-001"
    assert handoff.execution_id == "EXEC-001"
    assert handoff.activity_id == "ACTIVITY-001"
    assert handoff.evidence_ids == ("EVIDENCE-001",)
    assert handoff.contains_evidence("EVIDENCE-001")
    assert handoff.source_ids() == (
        "HANDOFF-001",
        "TRACE-001",
        "EXEC-001",
        "ACTIVITY-001",
        "EVIDENCE-001",
    )


def test_semantic_handoff_cannot_grant_authority() -> None:
    with pytest.raises(ValueError, match="cannot grant authority"):
        SemanticHandoff(
            handoff_id="HANDOFF-001",
            trace_id="TRACE-001",
            execution_id="EXEC-001",
            activity_id=None,
            evidence_ids=(),
            project=None,
            objective=None,
            protocol_ids=(),
            verification_scope=(),
            verification_status="pending",
            execution_authorized=True,
        )


def test_semantic_handoff_requires_handoff_id() -> None:
    trace = _trace()
    trace_without_handoff = ExecutionTrace(
        trace_id=trace.trace_id,
        execution_id=trace.execution_id,
        handoff_id=None,
        evidence_ids=trace.evidence_ids,
        project=trace.project,
        objective=trace.objective,
        protocol_ids=trace.protocol_ids,
        verification_scope=trace.verification_scope,
    )
    with pytest.raises(ValueError, match="handoff_id"):
        SemanticHandoff.from_trace(trace_without_handoff)

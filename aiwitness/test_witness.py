from runtime.trace import ExecutionTrace
from aiwitness.witness import AIwitness, WitnessRecord
import pytest


def make_trace() -> ExecutionTrace:
    return ExecutionTrace(
        trace_id="TRACE-001",
        execution_id="EXEC-001",
        handoff_id="SH-HO-20260925-001",
        evidence_ids=("EVID-001",),
        project="Shirakami",
        objective="observe execution",
        protocol_ids=("P-001",),
        verification_scope=("test",),
        verification_status="pass",
        verification_uncertainty=None,
        verification_observed={"test": "passed"},
        commit="abc123",
    )


def test_aiwitness_preserves_trace_identity_and_evidence():
    trace = make_trace()
    witness = AIwitness.observe(trace)

    assert isinstance(witness, WitnessRecord)
    assert witness.trace_id == trace.trace_id
    assert witness.execution_id == trace.execution_id
    assert witness.handoff_id == trace.handoff_id
    assert witness.evidence_ids == trace.evidence_ids
    assert witness.verification_status == trace.verification_status
    assert witness.commit == trace.commit


def test_aiwitness_does_not_grant_authority():
    witness = AIwitness.observe(make_trace())

    assert witness.execution_authorized is False
    assert witness.publish_authorized is False
    assert witness.merge_authorized is False
    assert witness.human_gate_required is True


def test_aiwitness_does_not_modify_source_trace():
    trace = make_trace()
    before = trace
    witness = AIwitness.observe(trace)

    assert trace == before
    assert witness is not trace


def test_aiwitness_requires_handoff_identity():
    trace = make_trace()
    trace = ExecutionTrace(
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
        AIwitness.observe(trace)

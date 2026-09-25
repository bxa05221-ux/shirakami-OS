from __future__ import annotations

import pytest

from aiwitness.traceability import validate_comparative_traceability, validate_traceability


def records():
    trace = {
        "trace_id": "TRACE-1",
        "execution_id": "EXEC-1",
        "handoff_id": "SH-HO-1",
        "evidence_ids": ["E-1"],
        "verification_status": "pass",
        "commit": "abc123",
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }
    witness = {
        "witness_id": "WITNESS-1",
        "trace_id": "TRACE-1",
        "execution_id": "EXEC-1",
        "handoff_id": "SH-HO-1",
        "evidence_ids": ["E-1"],
        "verification_status": "pass",
        "commit": "abc123",
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }
    execution = {
        "trace_id": "TRACE-1",
        "execution_id": "EXEC-1",
        "handoff_id": "SH-HO-1",
        "evidence_ids": ["E-1"],
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }
    return trace, witness, execution


def comparative_context():
    return {
        "project_id": "project-1",
        "reviewer_ids": ["reviewer-a", "reviewer-b"],
        "shared_evidence_ids": ["E-1"],
        "divergent_evidence_ids": ["E-2", "E-3"],
        "observations": [
            {"reviewer_id": "reviewer-a", "proposal": {"action": "A"}},
            {"reviewer_id": "reviewer-b", "proposal": {"action": "B"}},
        ],
        "decision": None,
        "authority_granted": False,
        "decision_authorized": False,
        "human_gate_required": True,
    }


def test_traceability_preserves_identity_chain():
    trace, witness, execution = records()

    result = validate_traceability(
        trace=trace,
        witness=witness,
        execution=execution,
        evidence_ids=["E-1"],
    )

    assert result.evidence_ids == ("E-1",)
    assert result.handoff_id == "SH-HO-1"
    assert result.execution_id == "EXEC-1"
    assert result.trace_id == "TRACE-1"
    assert result.witness_id == "WITNESS-1"
    assert result.verification_status == "pass"
    assert result.commit == "abc123"
    assert result.execution_authorized is False
    assert result.publish_authorized is False
    assert result.merge_authorized is False
    assert result.human_gate_required is True


@pytest.mark.parametrize(
    "record_name, field",
    [
        ("trace", "execution_authorized"),
        ("witness", "publish_authorized"),
        ("execution", "merge_authorized"),
    ],
)
def test_traceability_rejects_authority(record_name, field):
    trace, witness, execution = records()
    {"trace": trace, "witness": witness, "execution": execution}[record_name][field] = True

    with pytest.raises(ValueError, match="authority"):
        validate_traceability(
            trace=trace,
            witness=witness,
            execution=execution,
            evidence_ids=["E-1"],
        )


def test_traceability_rejects_evidence_drift():
    trace, witness, execution = records()
    witness["evidence_ids"] = ["E-2"]

    with pytest.raises(ValueError, match="evidence_ids"):
        validate_traceability(
            trace=trace,
            witness=witness,
            execution=execution,
            evidence_ids=["E-1"],
        )


def test_traceability_rejects_identity_mismatch():
    trace, witness, execution = records()
    execution["trace_id"] = "TRACE-OTHER"

    with pytest.raises(ValueError, match="trace_id"):
        validate_traceability(
            trace=trace,
            witness=witness,
            execution=execution,
            evidence_ids=["E-1"],
        )


def test_traceability_rejects_verification_or_commit_drift():
    trace, witness, execution = records()
    witness["verification_status"] = "fail"

    with pytest.raises(ValueError, match="verification status"):
        validate_traceability(
            trace=trace,
            witness=witness,
            execution=execution,
            evidence_ids=["E-1"],
        )

    witness["verification_status"] = "pass"
    witness["commit"] = "other"

    with pytest.raises(ValueError, match="commit"):
        validate_traceability(
            trace=trace,
            witness=witness,
            execution=execution,
            evidence_ids=["E-1"],
        )


def test_comparative_traceability_preserves_proposals_without_decision():
    context = comparative_context()

    result = validate_comparative_traceability(context=context)

    assert result.project_id == "project-1"
    assert result.reviewer_ids == ("reviewer-a", "reviewer-b")
    assert result.shared_evidence_ids == ("E-1",)
    assert result.divergent_evidence_ids == ("E-2", "E-3")
    assert result.decision is None
    assert result.authority_granted is False
    assert result.decision_authorized is False
    assert result.human_gate_required is True
    assert context["observations"][0]["proposal"] == {"action": "A"}
    assert context["observations"][1]["proposal"] == {"action": "B"}


@pytest.mark.parametrize(
    "field, value, message",
    [
        ("decision", "approve", "decision"),
        ("authority_granted", True, "authority"),
        ("decision_authorized", True, "authorize"),
        ("human_gate_required", False, "human gate"),
    ],
)
def test_comparative_traceability_rejects_authority_escalation(
    field, value, message
):
    context = comparative_context()
    context[field] = value

    with pytest.raises(ValueError, match=message):
        validate_comparative_traceability(context=context)


def test_comparative_traceability_rejects_evidence_overlap():
    context = comparative_context()
    context["divergent_evidence_ids"] = ["E-1", "E-3"]

    with pytest.raises(ValueError, match="overlap"):
        validate_comparative_traceability(context=context)

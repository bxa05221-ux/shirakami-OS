import pytest

from runtime.approval_envelope import ApprovalEnvelope
from runtime.human_gate import HumanGateError, process_human_gate


def candidate():
    return {
        "candidate_identity": "candidate-test-001",
        "validation": True,
        "authority": False,
        "executable": False,
        "protocol_identity": "protocol-test-001",
        "provenance": ("generator-test", "source-test"),
        "evidence_ids": ("evidence-test-001",),
    }


def test_reject_creates_no_authority():
    result = process_human_gate(
        candidate=candidate(),
        reviewer_identity="human-test",
        decision="reject",
    )
    assert result.decision == "reject"
    assert result.approval_envelope is None


def test_approve_creates_immutable_execution_envelope():
    result = process_human_gate(
        candidate=candidate(),
        reviewer_identity="human-test",
        decision="approve",
    )
    assert result.decision == "approve"
    assert isinstance(result.approval_envelope, ApprovalEnvelope)
    assert result.approval_envelope.candidate_id == "candidate-test-001"
    assert result.approval_envelope.protocol_id == "protocol-test-001"
    assert result.approval_envelope.execution_authorized is True
    assert result.approval_envelope.publication_authorized is False
    assert result.approval_envelope.provenance == ("generator-test", "source-test")


@pytest.mark.parametrize("decision", ["", "pending", "auto", "approved"])
def test_invalid_decision_fails_closed(decision):
    with pytest.raises(HumanGateError):
        process_human_gate(
            candidate=candidate(),
            reviewer_identity="human-test",
            decision=decision,
        )


def test_missing_identity_fails_closed():
    c = candidate()
    del c["candidate_identity"]
    with pytest.raises(HumanGateError):
        process_human_gate(
            candidate=c,
            reviewer_identity="human-test",
            decision="approve",
        )


def test_nonvalidated_candidate_fails_closed():
    c = candidate()
    c["validation"] = False
    with pytest.raises(HumanGateError):
        process_human_gate(
            candidate=c,
            reviewer_identity="human-test",
            decision="approve",
        )


def test_approval_does_not_create_activation_scheduler_or_runner():
    result = process_human_gate(
        candidate=candidate(),
        reviewer_identity="human-test",
        decision="approve",
    )
    envelope = result.approval_envelope
    assert envelope is not None
    assert not hasattr(envelope, "activation")
    assert not hasattr(envelope, "scheduler")
    assert not hasattr(envelope, "runner")

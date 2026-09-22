import pytest

from runtime.human_gate import HumanGateError, process_human_gate


def candidate():
    return {
        "candidate_identity": "candidate-test-001",
        "validation": True,
        "authority": False,
        "executable": False,
    }


def test_reject_creates_no_authority():
    result = process_human_gate(
        candidate=candidate(),
        reviewer_identity="human-test",
        decision="reject",
    )
    assert result.decision == "reject"
    assert result.approval_envelope is None


def test_approve_requires_explicit_human_decision():
    result = process_human_gate(
        candidate=candidate(),
        reviewer_identity="human-test",
        decision="approve",
    )
    assert result.decision == "approve"
    assert result.approval_envelope["authority_source"] == "human_gate"
    assert result.approval_envelope["candidate_identity"] == "candidate-test-001"


@pytest.mark.parametrize("decision", ["", "pending", "auto", "approved"])
def test_invalid_decision_fails_closed(decision):
    with pytest.raises(HumanGateError):
        process_human_gate(
            candidate=candidate(),
            reviewer_identity="human-test",
            decision=decision,
        )


def test_validation_pass_does_not_implicitly_promote():
    c = candidate()
    assert c["authority"] is False
    assert c["executable"] is False


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

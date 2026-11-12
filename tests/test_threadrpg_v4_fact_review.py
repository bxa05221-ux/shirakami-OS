from runtime.human_gate import HumanGateDecision
from runtime.threadrpg_v4_fact_review import (
    prepare_fact_review,
    may_promote_to_fact,
)


def test_approval_without_authentication_cannot_promote():
    decision = HumanGateDecision("candidate-1", "approve", "reviewer-1")
    review = prepare_fact_review("evidence-1", "hello", decision)
    assert review.decision == "approve"
    assert review.authenticated is False
    assert may_promote_to_fact(review) is False


def test_rejection_cannot_promote():
    decision = HumanGateDecision("candidate-1", "reject", "reviewer-1")
    review = prepare_fact_review("evidence-1", "hello", decision)
    assert may_promote_to_fact(review) is False

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

def test_fact_review_evidence_binding():
    from runtime.aats import Thread, Post
    from runtime.evidence_store import EvidenceStore
    from runtime.threadrpg_v4_observation import observe_post, record_observation
    from runtime.threadrpg_v4_fact_review import fact_review_matches

    thread = Thread("t").with_post(Post("icchi", "hello"))
    thread = thread.with_post(Post("icchi", "different"))
    store = record_observation(
        thread, observe_post(thread, 0, origin="human_post"), EvidenceStore()
    )
    evidence_id = store.all()[0].evidence_id
    candidate_id = f"threadrpg.v4:t:0:{evidence_id}"
    decision = HumanGateDecision(candidate_id, "approve", "reviewer-1")
    review = prepare_fact_review(evidence_id, "hello", decision)

    assert fact_review_matches(review, decision, store, thread, 0)
    assert not fact_review_matches(review, decision, store, thread, 1)
    assert not fact_review_matches(
        review,
        HumanGateDecision("wrong-candidate", "approve", "reviewer-1"),
        store, thread, 0
    )
    assert not fact_review_matches(
        review,
        HumanGateDecision(candidate_id, "approve", "another-reviewer"),
        store, thread, 0
    )
    assert not may_promote_to_fact(review)

def test_forged_authentication_flag_cannot_promote():
    from runtime.threadrpg_v4_fact_review import FactReview

    forged = FactReview(
        evidence_id="evidence-1",
        candidate_text="hello",
        reviewer_identity="reviewer-1",
        decision="approve",
        authenticated=True,
    )
    assert may_promote_to_fact(forged) is False


def test_forged_approval_envelope_cannot_promote():
    from runtime.approval_envelope import ApprovalEnvelope
    from runtime.human_gate import HumanGateDecision
    from runtime.threadrpg_v4_fact_review import FactReview

    envelope = ApprovalEnvelope(
        candidate_id="candidate-1",
        protocol_id="threadrpg.v4",
    ).authorize_execution("reviewer-1")

    decision = HumanGateDecision(
        candidate_identity="candidate-1",
        decision="approve",
        reviewer_identity="reviewer-1",
        approval_envelope=envelope,
    )

    review = FactReview(
        evidence_id="evidence-1",
        candidate_text="hello",
        reviewer_identity=decision.reviewer_identity,
        decision=decision.decision,
        authenticated=True,
    )
    assert may_promote_to_fact(review) is False

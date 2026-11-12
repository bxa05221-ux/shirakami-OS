"""ThreadRPG v4 human approval boundary.

A HumanGateDecision is a decision record, not proof of reviewer identity.
This adapter does not grant fact authority.
"""
from dataclasses import dataclass

from runtime.human_gate import HumanGateDecision


@dataclass(frozen=True)
class FactReview:
    evidence_id: str
    candidate_text: str
    reviewer_identity: str
    decision: str
    authenticated: bool = False


def prepare_fact_review(
    evidence_id: str,
    candidate_text: str,
    gate_decision: HumanGateDecision,
) -> FactReview:
    if not isinstance(gate_decision, HumanGateDecision):
        raise TypeError("HumanGateDecision required")
    if not evidence_id or not candidate_text.strip():
        raise ValueError("evidence and candidate text required")
    if gate_decision.decision not in ("approve", "reject"):
        raise ValueError("invalid decision")

    return FactReview(
        evidence_id=evidence_id,
        candidate_text=candidate_text,
        reviewer_identity=gate_decision.reviewer_identity,
        decision=gate_decision.decision,
        authenticated=False,
    )


def may_promote_to_fact(review: FactReview) -> bool:
    """Fail closed until a trusted reviewer-authentication path exists."""
    return False

def fact_review_matches(
    review: FactReview,
    gate_decision: HumanGateDecision,
    store,
    thread,
    post_index: int,
) -> bool:
    """Check review provenance without granting fact authority."""
    from runtime.aats import Thread
    from runtime.evidence_store import EvidenceStore
    from runtime.threadrpg_v4_evidence_gate import observation_evidence_matches

    if not isinstance(review, FactReview):
        return False
    if not isinstance(gate_decision, HumanGateDecision):
        return False
    if not isinstance(store, EvidenceStore) or not isinstance(thread, Thread):
        return False
    if not isinstance(post_index, int) or isinstance(post_index, bool):
        return False
    if not 0 <= post_index < len(thread.posts):
        return False
    if review.decision != gate_decision.decision:
        return False
    if review.reviewer_identity != gate_decision.reviewer_identity:
        return False
    if gate_decision.candidate_identity != (
        f"threadrpg.v4:{thread.thread_id}:{post_index}:{review.evidence_id}"
    ):
        return False
    if review.candidate_text != thread.posts[post_index].text:
        return False

    return observation_evidence_matches(
        store, thread, post_index, review.evidence_id
    )

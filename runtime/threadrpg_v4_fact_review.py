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

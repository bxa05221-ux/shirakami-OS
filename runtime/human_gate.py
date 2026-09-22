from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class HumanGateDecision:
    candidate_identity: str
    decision: str
    reviewer_identity: str
    approval_envelope: Optional[Dict[str, Any]] = None


class HumanGateError(ValueError):
    pass


def process_human_gate(
    *,
    candidate: Dict[str, Any],
    reviewer_identity: str,
    decision: str,
) -> HumanGateDecision:
    """Process an explicit human decision without implicit promotion."""

    if candidate.get("authority") is not False:
        raise HumanGateError("candidate must have no authority")

    if candidate.get("executable") is not False:
        raise HumanGateError("candidate must not be executable")

    candidate_identity = candidate.get("candidate_identity")
    if not candidate_identity:
        raise HumanGateError("missing candidate identity")

    if candidate.get("validation") is not True:
        raise HumanGateError("candidate must have structural validation PASS")

    if not reviewer_identity:
        raise HumanGateError("missing reviewer identity")

    if decision not in {"approve", "reject"}:
        raise HumanGateError("invalid human decision")

    if decision == "reject":
        return HumanGateDecision(
            candidate_identity=candidate_identity,
            decision="reject",
            reviewer_identity=reviewer_identity,
            approval_envelope=None,
        )

    approval_envelope = {
        "candidate_identity": candidate_identity,
        "reviewer_identity": reviewer_identity,
        "authority_source": "human_gate",
        "immutable": True,
    }

    return HumanGateDecision(
        candidate_identity=candidate_identity,
        decision="approve",
        reviewer_identity=reviewer_identity,
        approval_envelope=approval_envelope,
    )

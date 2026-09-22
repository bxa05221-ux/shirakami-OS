from dataclasses import dataclass
from typing import Any, Dict, Optional

from runtime.approval_envelope import ApprovalEnvelope


@dataclass(frozen=True)
class HumanGateDecision:
    candidate_identity: str
    decision: str
    reviewer_identity: str
    approval_envelope: Optional[ApprovalEnvelope] = None


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

    protocol_id = candidate.get("protocol_identity")
    if not protocol_id:
        raise HumanGateError("missing explicit protocol identity")

    provenance = candidate.get("provenance", ())
    evidence_ids = candidate.get("evidence_ids", ())

    try:
        envelope = ApprovalEnvelope(
            candidate_id=candidate_identity,
            protocol_id=protocol_id,
            provenance=tuple(provenance),
            evidence_ids=tuple(evidence_ids),
        ).authorize_execution(reviewer_identity)
    except (TypeError, ValueError) as exc:
        raise HumanGateError(str(exc)) from exc

    return HumanGateDecision(
        candidate_identity=candidate_identity,
        decision="approve",
        reviewer_identity=reviewer_identity,
        approval_envelope=envelope,
    )

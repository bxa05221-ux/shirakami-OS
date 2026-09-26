"""Evidence promotion boundary for verified external Agent Activity.

Promotion is explicit: verification may make an activity eligible for Evidence,
but the boundary never grants authority. The original activity provenance is
embedded in the Evidence transition data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .agent_activity import AgentActivity
from .agent_activity_verification import ActivityVerification
from .evidence import EvidenceRecord


@dataclass(frozen=True)
class EvidencePromotion:
    activity_id: str
    evidence_id: str
    verification_method: str
    status: str


class AgentActivityEvidencePromoter:
    """Convert a verified external activity into an EvidenceRecord."""

    def promote(
        self,
        activity: AgentActivity,
        verification: ActivityVerification,
        *,
        human_gate_confirmed: bool = False,
    ) -> tuple[EvidenceRecord, EvidencePromotion]:
        if verification.activity_id != activity.activity_id:
            raise ValueError("verification does not match activity")
        if verification.status != "verified":
            raise ValueError("only verified activity may be promoted")
        if not human_gate_confirmed:
            raise ValueError("explicit Human Gate confirmation required")

        record = EvidenceRecord(
            protocol_id="external.agent.activity",
            status="verified",
            transition_kind="external_agent_activity",
            transition_data={
                "activity_id": activity.activity_id,
                "agent_id": activity.agent_id,
                "session_id": activity.session_id,
                "source": activity.source,
                "operation_type": activity.operation_type,
                "target": activity.target,
                "input": activity.input,
                "result": activity.result,
                "timestamp": activity.timestamp,
                "provenance": dict(activity.provenance),
                "self_reported": activity.self_reported,
                "verification": {
                    "status": verification.status,
                    "method": verification.method,
                    "observed": dict(verification.observed),
                    "uncertainty": verification.uncertainty,
                },
                "human_gate_confirmed": True,
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
                "human_gate_required": True,
            },
            signals=("EXTERNAL_AGENT_ACTIVITY", "VERIFIED_ACTIVITY"),
            confidence="verified",
        )

        return record, EvidencePromotion(
            activity_id=activity.activity_id,
            evidence_id=record.evidence_id,
            verification_method=verification.method,
            status="promoted",
        )

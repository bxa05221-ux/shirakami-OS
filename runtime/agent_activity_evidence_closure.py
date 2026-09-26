"""Trace closure for verified external Agent Activity Evidence."""

from __future__ import annotations

from dataclasses import dataclass

from .agent_activity import AgentActivity
from .agent_activity_evidence import AgentActivityEvidencePromoter, EvidencePromotion
from .agent_activity_verification import ActivityVerification
from .aiwitness.witness import AIwitness, WitnessRecord
from .evidence_store import EvidenceStore
from .trace import ExecutionTraceStore


@dataclass(frozen=True)
class AgentActivityEvidenceClosure:
    promotion: EvidencePromotion
    trace_id: str
    witness: WitnessRecord


class AgentActivityEvidenceCloser:
    """Close Activity -> Evidence -> Trace -> AIwitness without granting authority."""

    def __init__(self, traces: ExecutionTraceStore, evidence: EvidenceStore) -> None:
        self.traces = traces
        self.evidence = evidence
        self.promoter = AgentActivityEvidencePromoter()

    def close(
        self,
        activity: AgentActivity,
        verification: ActivityVerification,
        *,
        trace_id: str,
        human_gate_confirmed: bool = False,
    ) -> AgentActivityEvidenceClosure:
        record, promotion = self.promoter.promote(
            activity,
            verification,
            human_gate_confirmed=human_gate_confirmed,
        )
        trace = self.traces.get(trace_id)
        if trace is None:
            raise ValueError("trace does not exist")

        if trace.verification_observed.get("activity_id") != activity.activity_id:
            raise ValueError("trace does not match activity")

        self.evidence = self.evidence.append(record)
        updated = self.traces.attach_evidence(
            trace_id,
            record.evidence_id,
            observed={
                "evidence_registered": True,
                "evidence_id": record.evidence_id,
                "activity_id": activity.activity_id,
                "human_gate_confirmed": True,
            },
        )
        if updated is None:
            raise ValueError("trace disappeared during evidence attachment")

        witness = AIwitness.observe(updated)
        return AgentActivityEvidenceClosure(
            promotion=promotion,
            trace_id=updated.trace_id,
            witness=witness,
        )

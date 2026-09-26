"""Bridge external Agent Activity into Shirakami traceability.

This adapter creates a pending external-activity ExecutionTrace. It does not
create Evidence and does not grant authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from .agent_activity import AgentActivity, ActivityObservation
from .trace import ExecutionTrace, ExecutionTraceStore


@dataclass(frozen=True)
class AgentActivityTraceLink:
    activity_id: str
    handoff_id: str
    execution_id: str
    trace_id: str
    evidence_ids: tuple[str, ...] = ()


class AgentActivityTraceAdapter:
    """Link external Agent activity to Shirakami's trace boundary."""

    def __init__(self, traces: ExecutionTraceStore) -> None:
        self.traces = traces

    def ingest(
        self,
        activity: AgentActivity,
        *,
        handoff_id: str | None = None,
        project: str | None = None,
        objective: str | None = None,
    ) -> AgentActivityTraceLink:
        observation = ActivityObservation.from_activity(
            activity,
            handoff_id=handoff_id or f"HANDOFF-{uuid4()}",
        )
        execution_id = f"EXEC-{uuid4()}"
        trace_id = f"TRACE-{uuid4()}"

        trace = ExecutionTrace(
            trace_id=trace_id,
            execution_id=execution_id,
            handoff_id=observation.handoff_id,
            evidence_ids=(),
            project=project,
            objective=objective,
            protocol_ids=(),
            verification_scope=(
                "external_agent_activity",
                observation.operation_type,
                observation.target,
            ),
            verification_status="pending",
            verification_uncertainty=(
                "External Agent activity is self-reported or externally supplied; "
                "independent verification has not yet established the underlying operation."
            ),
            verification_observed={
                "activity_id": activity.activity_id,
                "actor_type": "external_agent",
                "agent_id": activity.agent_id,
                "session_id": activity.session_id,
                "source": activity.source,
                "operation_type": activity.operation_type,
                "target": activity.target,
                "self_reported": activity.self_reported,
                "external_verification_status": activity.verification_status,
                "evidence_registered": False,
            },
        )

        self.traces.create(trace)

        return AgentActivityTraceLink(
            activity_id=activity.activity_id,
            handoff_id=observation.handoff_id or "",
            execution_id=execution_id,
            trace_id=trace_id,
        )

"""Provider-neutral external Agent Activity ingestion boundary.

This module records an external Agent's reported activity as an unverified
observation candidate. It does not execute the activity, grant authority, or
promote the report to Evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Mapping


@dataclass(frozen=True)
class AgentActivity:
    """Immutable report of an activity that occurred outside Shirakami Runtime."""

    agent_id: str | None
    session_id: str | None
    source: str
    operation_type: str
    target: str | None
    input: Any | None
    result: Any | None
    timestamp: str | None
    provenance: Mapping[str, Any] = field(default_factory=dict)
    self_reported: bool = True
    verification_status: str = "unverified"
    activity_id: str = field(init=False)

    def __post_init__(self) -> None:
        canonical = json.dumps(
            {
                "agent_id": self.agent_id,
                "session_id": self.session_id,
                "source": self.source,
                "operation_type": self.operation_type,
                "target": self.target,
                "input": self.input,
                "result": self.result,
                "timestamp": self.timestamp,
                "provenance": dict(self.provenance),
                "self_reported": self.self_reported,
                "verification_status": self.verification_status,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")
        object.__setattr__(
            self,
            "activity_id",
            hashlib.sha256(canonical).hexdigest(),
        )


@dataclass(frozen=True)
class ActivityObservation:
    """Observation candidate derived from an external Agent Activity report."""

    activity_id: str
    source: str
    operation_type: str
    target: str | None
    verification_status: str
    provenance: Mapping[str, Any]
    self_reported: bool
    handoff_id: str | None = None

    @classmethod
    def from_activity(
        cls,
        activity: AgentActivity,
        *,
        handoff_id: str | None = None,
    ) -> "ActivityObservation":
        return cls(
            activity_id=activity.activity_id,
            source=activity.source,
            operation_type=activity.operation_type,
            target=activity.target,
            verification_status=activity.verification_status,
            provenance=activity.provenance,
            self_reported=activity.self_reported,
            handoff_id=handoff_id,
        )


def ingest_agent_activity(
    *,
    agent_id: str | None,
    session_id: str | None,
    source: str,
    operation_type: str,
    target: str | None = None,
    input: Any | None = None,
    result: Any | None = None,
    timestamp: str | None = None,
    provenance: Mapping[str, Any] | None = None,
    self_reported: bool = True,
) -> AgentActivity:
    """Create an unverified external activity record.

    This is intentionally an ingestion boundary, not an execution boundary.
    """
    return AgentActivity(
        agent_id=agent_id,
        session_id=session_id,
        source=source,
        operation_type=operation_type,
        target=target,
        input=input,
        result=result,
        timestamp=timestamp,
        provenance=provenance or {},
        self_reported=self_reported,
    )

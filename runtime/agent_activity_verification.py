"""Verification boundary for externally reported Agent Activity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .agent_activity import AgentActivity
from .trace import ExecutionTraceStore


@dataclass(frozen=True)
class ActivityVerification:
    activity_id: str
    status: str
    method: str
    observed: Mapping[str, Any]
    uncertainty: str


class AgentActivityVerifier:
    """Apply independent verification metadata without creating authority."""

    def verify(
        self,
        activity: AgentActivity,
        *,
        method: str,
        verified: bool,
        observed: Mapping[str, Any] | None = None,
        uncertainty: str = "",
    ) -> ActivityVerification:
        return ActivityVerification(
            activity_id=activity.activity_id,
            status="verified" if verified else "unverified",
            method=method,
            observed=observed or {},
            uncertainty=uncertainty,
        )


class AgentActivityTraceVerifier:
    """Attach verification to an existing external-activity trace."""

    def __init__(self, traces: ExecutionTraceStore) -> None:
        self.traces = traces

    def attach(
        self,
        trace_id: str,
        verification: ActivityVerification,
    ):
        current = self.traces.get(trace_id)
        if current is None:
            return None

        observed = dict(current.verification_observed)
        observed["verification"] = {
            "status": verification.status,
            "method": verification.method,
            "observed": dict(verification.observed),
        }

        return self.traces.attach_verification(
            trace_id,
            status=verification.status,
            uncertainty=verification.uncertainty,
            observed=observed,
        )

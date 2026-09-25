"""Immutable execution-to-evidence trace boundary.

A trace links an externally addressable execution to its semantic provenance
without creating execution, publication, or merge authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class ExecutionTrace:
    """Immutable provenance record for one execution."""

    trace_id: str
    execution_id: str
    handoff_id: str | None
    evidence_ids: tuple[str, ...]
    project: str | None
    objective: str | None
    protocol_ids: tuple[str, ...]
    verification_scope: tuple[Any, ...]
    verification_status: str = "pending"
    verification_uncertainty: str | None = None
    verification_observed: Mapping[str, Any] = None  # type: ignore[assignment]
    commit: str | None = None
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False
    human_gate_required: bool = True

    def __post_init__(self) -> None:
        if not self.trace_id:
            raise ValueError("trace_id must be non-empty")
        if not self.execution_id:
            raise ValueError("execution_id must be non-empty")
        if self.execution_authorized or self.publish_authorized or self.merge_authorized:
            raise ValueError("trace cannot grant authority")
        if not self.human_gate_required:
            raise ValueError("human_gate_required must remain true")
        if self.verification_observed is None:
            object.__setattr__(self, "verification_observed", {})

    def with_verification(self, status: str, uncertainty: str, observed: Mapping[str, Any]) -> "ExecutionTrace":
        return ExecutionTrace(
            trace_id=self.trace_id,
            execution_id=self.execution_id,
            handoff_id=self.handoff_id,
            evidence_ids=self.evidence_ids,
            project=self.project,
            objective=self.objective,
            protocol_ids=self.protocol_ids,
            verification_scope=self.verification_scope,
            verification_status=status,
            verification_uncertainty=uncertainty,
            verification_observed=dict(observed),
            commit=self.commit,
        )


class ExecutionTraceStore:
    """In-memory append-only trace history."""

    def __init__(self) -> None:
        self._records: dict[str, list[ExecutionTrace]] = {}

    def create(self, trace: ExecutionTrace) -> ExecutionTrace:
        self._records.setdefault(trace.trace_id, []).append(trace)
        return trace

    def get(self, trace_id: str) -> ExecutionTrace | None:
        records = self._records.get(trace_id)
        return records[-1] if records else None

    def attach_verification(
        self,
        trace_id: str,
        *,
        status: str,
        uncertainty: str,
        observed: Mapping[str, Any],
    ) -> ExecutionTrace | None:
        current = self.get(trace_id)
        if current is None:
            return None
        updated = current.with_verification(status, uncertainty, observed)
        self._records[trace_id].append(updated)
        return updated

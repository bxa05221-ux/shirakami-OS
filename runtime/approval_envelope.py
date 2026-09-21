"""Shared approval handoff envelope for Shirakami runtime boundaries.

The envelope carries provenance and human authorization metadata without
selecting a Protocol, authorizing execution implicitly, or granting publication
permission as a side effect.
"""

from dataclasses import dataclass, field
from typing import Any, Mapping


class ApprovalEnvelopeError(ValueError):
    """Raised when an approval envelope violates its safety boundary."""


@dataclass(frozen=True)
class ApprovalEnvelope:
    """Immutable handoff metadata shared across Protocol boundaries."""

    candidate_id: str
    protocol_id: str
    provenance: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    reviewer: str | None = None
    approval_scope: str | None = None
    execution_authorized: bool = False
    publication_authorized: bool = False
    context: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ApprovalEnvelopeError("candidate_id is required")
        if not self.protocol_id.strip():
            raise ApprovalEnvelopeError("protocol_id is required")
        if self.execution_authorized and not self.reviewer:
            raise ApprovalEnvelopeError(
                "execution authorization requires an identified reviewer"
            )
        if self.publication_authorized and not self.execution_authorized:
            raise ApprovalEnvelopeError(
                "publication authorization requires execution authorization"
            )
        if self.publication_authorized and self.approval_scope != "publication":
            raise ApprovalEnvelopeError(
                "publication authorization requires publication scope"
            )

    def authorize_execution(self, reviewer: str, scope: str = "execution") -> "ApprovalEnvelope":
        if not reviewer.strip():
            raise ApprovalEnvelopeError("reviewer is required")
        if scope not in {"execution", "publication"}:
            raise ApprovalEnvelopeError("scope must be execution or publication")
        return ApprovalEnvelope(
            candidate_id=self.candidate_id,
            protocol_id=self.protocol_id,
            provenance=self.provenance,
            evidence_ids=self.evidence_ids,
            reviewer=reviewer,
            approval_scope=scope,
            execution_authorized=True,
            publication_authorized=False,
            context=dict(self.context),
        )

    def authorize_publication(self, reviewer: str) -> "ApprovalEnvelope":
        if not self.execution_authorized:
            raise ApprovalEnvelopeError("execution authorization is required first")
        if self.approval_scope != "publication":
            raise ApprovalEnvelopeError("publication scope must be granted explicitly")
        return ApprovalEnvelope(
            candidate_id=self.candidate_id,
            protocol_id=self.protocol_id,
            provenance=self.provenance,
            evidence_ids=self.evidence_ids,
            reviewer=reviewer,
            approval_scope="publication",
            execution_authorized=True,
            publication_authorized=True,
            context=dict(self.context),
        )

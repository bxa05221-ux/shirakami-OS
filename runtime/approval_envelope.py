"""Shared approval handoff envelope for Shirakami runtime boundaries."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


class ApprovalEnvelopeError(ValueError):
    """Raised when an approval envelope violates its safety boundary."""


def _freeze(value: Any) -> Any:
    """Recursively freeze supported container values."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, set):
        return frozenset(_freeze(item) for item in value)
    return value


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
        object.__setattr__(self, "context", _freeze(self.context))
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

    def authorize_execution(
        self, reviewer: str, scope: str = "execution"
    ) -> "ApprovalEnvelope":
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
            context=self.context,
        )

    def authorize_publication(self, reviewer: str) -> "ApprovalEnvelope":
        if not reviewer.strip():
            raise ApprovalEnvelopeError("reviewer is required")
        if reviewer != self.reviewer:
            raise ApprovalEnvelopeError("publication reviewer must match execution reviewer")
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
            context=self.context,
        )

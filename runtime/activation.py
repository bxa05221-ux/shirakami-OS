"""Explicit activation boundary for already-authorized Protocols.

Activation prepares an authorized Protocol for Runtime execution. It never
creates approval or promotes a candidate.
"""

from dataclasses import dataclass, field
from typing import Any, Mapping

try:
    from .approval_envelope import ApprovalEnvelope, ApprovalEnvelopeError
except ImportError:
    from approval_envelope import ApprovalEnvelope, ApprovalEnvelopeError


class ActivationError(RuntimeError):
    """Raised when an activation request violates the authorization boundary."""


@dataclass(frozen=True)
class ActivationRequest:
    """A request to prepare an already-authorized Protocol for execution."""

    protocol_id: str
    approval: ApprovalEnvelope
    context: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.protocol_id:
            raise ActivationError("protocol_id is required")
        if not self.approval.execution_authorized:
            raise ActivationError("activation requires explicit execution authorization")
        if self.approval.protocol_id != self.protocol_id:
            raise ActivationError("approval envelope does not match protocol")
        if self.approval.candidate_id != self.approval.protocol_id:
            raise ActivationError(
                "activation requires a promoted Approved Protocol identity"
            )


@dataclass(frozen=True)
class ActivationResult:
    """Observable result of preparing an authorized Protocol."""

    protocol_id: str
    status: str
    context: Mapping[str, Any]


def activate(
    protocol_id: str,
    approval: ApprovalEnvelope,
    *,
    context: Mapping[str, Any] | None = None,
) -> ActivationResult:
    """Prepare an explicitly authorized Protocol for Runtime execution."""

    try:
        request = ActivationRequest(
            protocol_id=protocol_id,
            approval=approval,
            context=context or {},
        )
    except (ActivationError, ApprovalEnvelopeError):
        raise

    return ActivationResult(
        protocol_id=request.protocol_id,
        status="activated",
        context=request.context,
    )

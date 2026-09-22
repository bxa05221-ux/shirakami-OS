from dataclasses import dataclass
from typing import Any, Mapping


class ActivationError(ValueError):
    pass


@dataclass(frozen=True)
class Activation:
    candidate_id: str
    protocol_id: str
    approval_reviewer: str
    activation_id: str
    lifecycle_event: str = "activated_execution"
    released: bool = False


def activate_approved_protocol(
    *,
    approval: Mapping[str, Any],
    activation_id: str,
) -> Activation:
    """Prepare an activation from an already human-authorized envelope.

    Activation consumes authority; it never creates, expands, or transfers it.
    """

    if not isinstance(approval, Mapping):
        raise ActivationError("approval envelope is required")

    if approval.get("execution_authorized") is not True:
        raise ActivationError("execution authorization is required")

    if not approval.get("candidate_id"):
        raise ActivationError("candidate identity is required")

    if not approval.get("protocol_id"):
        raise ActivationError("protocol identity is required")

    if not approval.get("reviewer"):
        raise ActivationError("approval reviewer is required")

    if approval.get("approval_scope") not in {"execution", "publication"}:
        raise ActivationError("approval scope is required for activation")

    if not activation_id.strip():
        raise ActivationError("activation identity is required")

    return Activation(
        candidate_id=approval["candidate_id"],
        protocol_id=approval["protocol_id"],
        approval_reviewer=approval["reviewer"],
        activation_id=activation_id,
    )

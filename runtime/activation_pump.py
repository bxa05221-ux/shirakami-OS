from dataclasses import dataclass


class ActivationPumpError(ValueError):
    pass


@dataclass(frozen=True)
class ReleasedActivation:
    activation_id: str
    candidate_id: str
    protocol_id: str
    approval_reviewer: str
    lifecycle_event: str = "activated_execution"
    release_id: str = ""


def release_activation(
    *,
    activation,
    release_id: str,
) -> ReleasedActivation:
    """Release an already prepared Activation without creating authority."""

    if activation is None:
        raise ActivationPumpError("activation is required")

    if activation.released is True:
        raise ActivationPumpError("activation has already been released")

    if not activation.activation_id:
        raise ActivationPumpError("activation identity is required")

    if not release_id.strip():
        raise ActivationPumpError("release identity is required")

    return ReleasedActivation(
        activation_id=activation.activation_id,
        candidate_id=activation.candidate_id,
        protocol_id=activation.protocol_id,
        approval_reviewer=activation.approval_reviewer,
        release_id=release_id,
    )

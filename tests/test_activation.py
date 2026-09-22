import pytest

from runtime.activation import ActivationError, activate_approved_protocol


def approval():
    return {
        "candidate_id": "candidate-test-001",
        "protocol_id": "protocol-test-001",
        "reviewer": "human-test",
        "execution_authorized": True,
        "approval_scope": "execution",
    }


def test_only_approved_envelope_can_activate():
    activation = activate_approved_protocol(
        approval=approval(),
        activation_id="activation-test-001",
    )
    assert activation.candidate_id == "candidate-test-001"
    assert activation.protocol_id == "protocol-test-001"
    assert activation.lifecycle_event == "activated_execution"
    assert activation.released is False


@pytest.mark.parametrize("approval_field", ["execution_authorized"])
def test_missing_authority_fails_closed(approval_field):
    a = approval()
    a.pop(approval_field)
    with pytest.raises(ActivationError):
        activate_approved_protocol(
            approval=a,
            activation_id="activation-test-001",
        )


def test_unapproved_envelope_fails_closed():
    a = approval()
    a["execution_authorized"] = False
    with pytest.raises(ActivationError):
        activate_approved_protocol(
            approval=a,
            activation_id="activation-test-001",
        )


def test_missing_approval_scope_fails_closed():
    a = approval()
    a.pop("approval_scope")
    with pytest.raises(ActivationError):
        activate_approved_protocol(
            approval=a,
            activation_id="activation-test-001",
        )


def test_activation_does_not_release_or_schedule_execution():
    activation = activate_approved_protocol(
        approval=approval(),
        activation_id="activation-test-001",
    )
    assert activation.released is False

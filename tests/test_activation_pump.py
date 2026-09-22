import pytest

from runtime.activation import Activation
from runtime.activation_pump import ActivationPumpError, release_activation


def activation():
    return Activation(
        candidate_id="candidate-test-001",
        protocol_id="protocol-test-001",
        approval_reviewer="human-test",
        activation_id="activation-test-001",
    )


def test_pump_releases_prepared_activation():
    released = release_activation(
        activation=activation(),
        release_id="release-test-001",
    )
    assert released.activation_id == "activation-test-001"
    assert released.candidate_id == "candidate-test-001"
    assert released.protocol_id == "protocol-test-001"
    assert released.lifecycle_event == "activated_execution"


def test_pump_does_not_create_authority():
    released = release_activation(
        activation=activation(),
        release_id="release-test-001",
    )
    assert not hasattr(released, "approval_envelope")
    assert not hasattr(released, "reviewer")


def test_released_activation_cannot_be_released_again():
    a = activation()
    a = Activation(
        candidate_id=a.candidate_id,
        protocol_id=a.protocol_id,
        approval_reviewer=a.approval_reviewer,
        activation_id=a.activation_id,
        released=True,
    )
    with pytest.raises(ActivationPumpError):
        release_activation(activation=a, release_id="release-test-002")


def test_missing_activation_fails_closed():
    with pytest.raises(ActivationPumpError):
        release_activation(activation=None, release_id="release-test-001")

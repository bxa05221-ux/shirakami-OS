import pytest

from runtime.activation import activate
from runtime.activation_pump import (
    ActivationPump,
    ActivationPumpError,
    release_activation,
)
from runtime.approval_envelope import ApprovalEnvelope


def _activated(protocol_id="protocol-1"):
    envelope = ApprovalEnvelope(protocol_id, protocol_id).authorize_execution("human")
    return activate(protocol_id, envelope, context={"source": "human-gate"})


def test_pump_releases_only_activated_results():
    pump = ActivationPump()
    release = pump.release(_activated())

    assert release.protocol_id == "protocol-1"
    assert release.status == "released"
    assert release.context == {"source": "human-gate"}
    assert release.release_id


def test_pump_fails_closed_for_non_activated_result():
    pump = ActivationPump()
    activation = _activated()

    invalid = type(activation)(
        protocol_id=activation.protocol_id,
        status="prepared",
        context=activation.context,
    )

    with pytest.raises(ActivationPumpError, match="activated Protocol"):
        pump.release(invalid)


def test_pump_does_not_change_protocol_identity():
    activation = _activated("protocol-identity")
    release = release_activation(activation)

    assert release.protocol_id == activation.protocol_id


def test_pump_release_has_distinct_event_identity():
    activation = _activated()
    first = release_activation(activation)
    second = release_activation(activation)

    assert first.release_id != second.release_id
    assert first.protocol_id == second.protocol_id


def test_pump_copies_context_without_mutating_activation():
    activation = _activated()
    release = release_activation(activation)

    assert release.context == activation.context
    assert release.context is not activation.context

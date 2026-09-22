import pytest

from runtime.activation import activate
from runtime.activation_pump import release_activation
from runtime.evolution_pipeline import EvidenceDrivenRuntime
from runtime.approval_envelope import ApprovalEnvelope
from runtime.pump_cycle import PumpCycleError, execute_released_cycle
from runtime.prototype import Transition


def _release():
    envelope = ApprovalEnvelope("protocol-1", "protocol-1").authorize_execution("human")
    activation = activate("protocol-1", envelope, context={"source": "pump"})
    return release_activation(activation)


def test_released_cycle_reaches_verification_and_evidence():
    runtime = EvidenceDrivenRuntime()
    release = _release()

    def protocol(context):
        return Transition(
            kind="pump.evidence.transition",
            data={"input": dict(context.input)},
        )

    execution, verification = execute_released_cycle(
        release,
        runtime,
        protocol,
        expected_transition_kind="pump.evidence.transition",
    )

    assert execution.status == "completed"
    assert verification.status == "pass"
    assert any(
        record.protocol_id == "protocol-1"
        for record in runtime.store.all()
    )


def test_released_cycle_rejects_non_released_event():
    release = _release()
    invalid = type(release)(
        release_id=release.release_id,
        protocol_id=release.protocol_id,
        status="queued",
        context=release.context,
    )

    with pytest.raises(PumpCycleError, match="released Pump event"):
        execute_released_cycle(
            invalid,
            EvidenceDrivenRuntime(),
            lambda context: Transition(kind="unexpected", data={}),
        )


def test_released_cycle_preserves_protocol_identity_on_mismatch():
    runtime = EvidenceDrivenRuntime()
    release = _release()

    def protocol(context):
        return Transition(kind="unexpected", data={})

    execution, verification = execute_released_cycle(
        release,
        runtime,
        protocol,
        expected_transition_kind="expected",
    )

    assert execution.protocol_id == release.protocol_id
    assert verification.status == "mismatch"

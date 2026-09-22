import pytest

from runtime.activation import ActivationResult, activate
from runtime.activation_pump import release_activation
from runtime.approval_envelope import ApprovalEnvelope
from runtime.background_runner import BackgroundRunner
from runtime.evolution_pipeline import EvidenceDrivenRuntime
from runtime.prototype import Transition


def _release():
    envelope = ApprovalEnvelope("protocol-boundary", "protocol-boundary").authorize_execution("human")
    activation = activate(
        "protocol-boundary",
        envelope,
        context={"source": "boundary"},
    )
    return release_activation(activation)


def test_runtime_cannot_execute_from_idle_without_activation_binding():
    runtime = EvidenceDrivenRuntime()

    with pytest.raises(RuntimeError, match="runtime not ready for execution"):
        runtime.execute(
            lambda context: Transition(kind="unauthorized", data={}),
            "protocol-boundary",
            {},
        )


def test_activation_binding_does_not_create_approval():
    runtime = EvidenceDrivenRuntime()
    runtime.bind_activated_execution("protocol-boundary")

    assert runtime.loop.state.value == "READY"
    assert not any(
        record.event in {"approve", "review"}
        for record in runtime.loop.records
    )


def test_runner_reaches_evidence_and_preserves_authority_boundary():
    runtime = EvidenceDrivenRuntime()
    release = _release()

    results = BackgroundRunner().run(
        release,
        runtime,
        lambda context: Transition(
            kind="boundary.transition",
            data={"source": context.input["source"]},
        ),
        iterations=2,
        expected_transition_kind="boundary.transition",
    )

    assert len(results) == 2
    assert all(item.protocol_id == release.protocol_id for item in results)
    assert all(item.verification.status == "pass" for item in results)
    assert any(
        record.protocol_id == release.protocol_id
        for record in runtime.store.all()
    )


def test_runner_mismatch_cannot_be_promoted_to_success():
    runtime = EvidenceDrivenRuntime()
    release = _release()

    results = BackgroundRunner().run(
        release,
        runtime,
        lambda context: Transition(kind="wrong", data={}),
        iterations=5,
        expected_transition_kind="expected",
    )

    assert len(results) == 1
    assert results[0].verification.status == "mismatch"

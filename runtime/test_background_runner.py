import pytest

from runtime.activation import activate
from runtime.activation_pump import release_activation
from runtime.approval_envelope import ApprovalEnvelope
from runtime.background_runner import BackgroundRunner, BackgroundRunnerError
from runtime.evolution_pipeline import EvidenceDrivenRuntime
from runtime.prototype import Transition


def _release():
    envelope = ApprovalEnvelope("protocol-1", "protocol-1").authorize_execution("human")
    activation = activate("protocol-1", envelope, context={"source": "runner"})
    return release_activation(activation)


def test_runner_consumes_only_released_activation():
    runtime = EvidenceDrivenRuntime()
    release = _release()

    def protocol(context):
        return Transition(kind="runner.transition", data=dict(context.input))

    result = BackgroundRunner().run(
        release,
        runtime,
        protocol,
        expected_transition_kind="runner.transition",
    )

    assert len(result) == 1
    assert result[0].protocol_id == "protocol-1"
    assert result[0].status == "completed"
    assert result[0].verification.status == "pass"


def test_runner_supports_bounded_iterations():
    runtime = EvidenceDrivenRuntime()
    release = _release()

    def protocol(context):
        return Transition(kind="runner.loop", data={"source": context.input["source"]})

    result = BackgroundRunner().run(
        release,
        runtime,
        protocol,
        iterations=3,
        expected_transition_kind="runner.loop",
    )

    assert len(result) == 3
    assert [item.iteration for item in result] == [1, 2, 3]
    assert len({item.run_id for item in result}) == 1


def test_runner_stops_after_verification_mismatch():
    runtime = EvidenceDrivenRuntime()
    release = _release()

    result = BackgroundRunner().run(
        release,
        runtime,
        lambda context: Transition(kind="unexpected", data={}),
        iterations=3,
        expected_transition_kind="expected",
    )

    assert len(result) == 1
    assert result[0].verification.status == "mismatch"


def test_runner_rejects_non_released_event():
    release = _release()
    invalid = type(release)(
        release_id=release.release_id,
        protocol_id=release.protocol_id,
        status="queued",
        context=release.context,
    )

    with pytest.raises(BackgroundRunnerError, match="released Pump event"):
        BackgroundRunner().run(
            invalid,
            EvidenceDrivenRuntime(),
            lambda context: Transition(kind="unexpected", data={}),
        )


def test_runner_rejects_invalid_iteration_budget():
    with pytest.raises(BackgroundRunnerError, match="iterations"):
        BackgroundRunner().run(
            _release(),
            EvidenceDrivenRuntime(),
            lambda context: Transition(kind="unexpected", data={}),
            iterations=0,
        )


def test_runner_preserves_protocol_identity():
    runtime = EvidenceDrivenRuntime()
    release = _release()

    result = BackgroundRunner().run(
        release,
        runtime,
        lambda context: Transition(kind="runner.identity", data={}),
        iterations=2,
        expected_transition_kind="runner.identity",
    )

    assert all(item.protocol_id == release.protocol_id for item in result)

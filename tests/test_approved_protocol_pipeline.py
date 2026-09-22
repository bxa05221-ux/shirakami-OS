from runtime.activation_pump import release_activation
from runtime.approved_protocol_pipeline import PipelineError, run_approved_pipeline
from runtime.approval_envelope_activation import to_activation_input
from runtime.approval_envelope import ApprovalEnvelope
from runtime.activation import activate_approved_protocol


def released(candidate, protocol, reviewer, activation_id, release_id):
    envelope = ApprovalEnvelope(
        candidate_id=candidate,
        protocol_id=protocol,
    ).authorize_execution(reviewer)
    activation = activate_approved_protocol(
        approval=to_activation_input(envelope),
        activation_id=activation_id,
    )
    return release_activation(activation=activation, release_id=release_id)


def test_pipeline_preserves_explicit_order_and_identity():
    first = released("c1", "p1", "r1", "a1", "rel1")
    second = released("c2", "p2", "r2", "a2", "rel2")
    seen = []

    result = run_approved_pipeline(
        pipeline_identity="pipeline-001",
        activations=(first, second),
        execute=lambda activation, order: seen.append(
            (activation.activation_id, order)
        ) or "ok",
    )

    assert seen == [("a1", 1), ("a2", 2)]
    assert [item.protocol_identity for item in result.items] == ["p1", "p2"]
    assert result.stopped is False


def test_pipeline_stops_on_failure_and_does_not_run_later_activation():
    first = released("c1", "p1", "r1", "a1", "rel1")
    second = released("c2", "p2", "r2", "a2", "rel2")
    seen = []

    def execute(activation, order):
        seen.append(activation.activation_id)
        if order == 1:
            raise RuntimeError("verification mismatch")
        return "must-not-run"

    result = run_approved_pipeline(
        pipeline_identity="pipeline-002",
        activations=(first, second),
        execute=execute,
    )

    assert result.stopped is True
    assert seen == ["a1"]
    assert len(result.items) == 1


def test_pipeline_rejects_non_released_input():
    try:
        run_approved_pipeline(
            pipeline_identity="pipeline-003",
            activations=({"activation_id": "a1"},),
            execute=lambda activation, order: None,
        )
    except PipelineError:
        pass
    else:
        raise AssertionError("unreleased input must fail closed")

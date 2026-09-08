from runtime.checkpoint_delta_execution import execute_from_checkpoint
from runtime.evidence import capture_evidence
from runtime.prototype import ExecutionResult, Transition


def record(key, value):
    return capture_evidence(
        ExecutionResult(
            status="completed",
            protocol_id="example.protocol",
            transition=Transition(
                kind="matome.protocol.transition",
                data={key: value, "changed": True},
            ),
        )
    )


def test_execute_from_checkpoint_applies_only_delta():
    first = record("first", 1)
    second = record("second", 2)
    third = record("third", 3)

    state = execute_from_checkpoint(
        {"seed": "checkpoint"},
        [first, second, third],
        [first, second],
    )

    assert state.snapshot() == {
        "seed": "checkpoint",
        "third": 3,
        "changed": True,
    }
    assert state.evidence == (third,)

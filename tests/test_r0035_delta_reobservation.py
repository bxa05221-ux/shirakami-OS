from runtime.adapter import MemoryAdapter, adapt_landscape_observation
from runtime.delta_reobservation import execute_and_reobserve
from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
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


def test_execute_and_reobserve_reports_after_state():
    first = record("first", 1)
    second = record("second", 2)
    third = record("third", 3)

    result = execute_and_reobserve(
        {"seed": "checkpoint"},
        [first, second, third],
        [first, second],
        MemoryAdapter(),
    )

    assert result["snapshot"] == {
        "seed": "checkpoint",
        "third": 3,
        "changed": True,
    }
    assert result["observation"]["snapshot"] == result["snapshot"]

    expected_state = LandscapeState.from_snapshot({"seed": "checkpoint"})
    expected_state.apply_evidence(third)
    expected_observation = adapt_landscape_observation(expected_state)
    assert result["observation"] == expected_observation

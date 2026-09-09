from runtime.landscape import LandscapeState
from runtime.observable_execution import execute_observably
from runtime.prototype import Runtime, example_protocol


def test_r0069_two_sequential_operations_preserve_landscape_and_evidence_continuity():
    state = LandscapeState.from_snapshot(
        {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}
    )

    first = execute_observably(
        state,
        Runtime(),
        "example.protocol",
        example_protocol,
        {"message": "r0069-first"},
    )
    second = execute_observably(
        state,
        Runtime(),
        "example.protocol",
        example_protocol,
        {"message": "r0069-second"},
    )

    assert first.evidence.protocol_id == "example.protocol"
    assert second.evidence.protocol_id == "example.protocol"
    assert first.evidence != second.evidence
    assert first.after_state["input"] == {"message": "r0069-first"}
    assert second.before_state["input"] == {"message": "r0069-first"}
    assert second.after_state["input"] == {"message": "r0069-second"}
    assert second.observation["snapshot"]["input"] == {"message": "r0069-second"}
    assert len(state.evidence) == 2
    assert [e.protocol_id for e in state.evidence] == [
        "example.protocol",
        "example.protocol",
    ]
    assert second.observation["evidence_lineage"][-1]["protocol_id"] == "example.protocol"

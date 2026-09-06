from runtime.landscape import LandscapeState
from runtime.landscape_execution import execute_on_landscape
from runtime.prototype import Runtime, example_protocol


def test_execute_on_landscape_applies_evidence_to_existing_state():
    state = LandscapeState.from_snapshot({"repository": "bxa05221-ux/shirakami-OS", "branch": "main"})
    evidence = execute_on_landscape(
        state,
        Runtime(),
        "example.protocol",
        example_protocol,
        {"message": "hello landscape"},
    )

    assert evidence.protocol_id == "example.protocol"
    assert evidence.transition_kind == "example.transition"
    assert state.snapshot()["repository"] == "bxa05221-ux/shirakami-OS"
    assert state.snapshot()["input"] == {"message": "hello landscape"}
    assert state.snapshot()["changed"] is True
    assert state.evidence == [evidence]

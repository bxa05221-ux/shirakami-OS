from runtime.landscape import LandscapeState
from runtime.observable_execution import execute_observably
from runtime.prototype import Runtime, example_protocol


def test_r0068_one_operational_change_preserves_observable_continuity():
    state = LandscapeState.from_snapshot(
        {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}
    )
    before = state.snapshot()

    result = execute_observably(
        state,
        Runtime(),
        "example.protocol",
        example_protocol,
        {"message": "r0068 operational change"},
    )

    assert result.before_state == before
    assert result.evidence.protocol_id == "example.protocol"
    assert result.evidence.transition_kind == "example.transition"
    assert result.after_state["repository"] == "bxa05221-ux/shirakami-OS"
    assert result.after_state["branch"] == "main"
    assert result.after_state["input"] == {"message": "r0068 operational change"}
    assert result.after_state["changed"] is True
    assert result.observation["snapshot"]["repository"] == "bxa05221-ux/shirakami-OS"
    assert result.observation["snapshot"]["branch"] == "main"
    assert result.observation["snapshot"]["input"] == {"message": "r0068 operational change"}
    assert result.observation["snapshot"]["changed"] is True
    assert len(result.observation["evidence_lineage"]) == 1
    assert result.observation["evidence_lineage"][0]["protocol_id"] == "example.protocol"
    assert state.evidence == [result.evidence]

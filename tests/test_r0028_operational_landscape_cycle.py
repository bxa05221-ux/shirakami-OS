from runtime.landscape import LandscapeState
from runtime.observable_execution import execute_observably
from runtime.prototype import Runtime, example_protocol


def test_r0028_operational_cycle_is_inspectable():
    state = LandscapeState.from_snapshot(
        {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}
    )
    result = execute_observably(
        state,
        Runtime(),
        "example.protocol",
        example_protocol,
        {"operation": "operational-observation"},
    )

    assert result.before_state["repository"] == "bxa05221-ux/shirakami-OS"
    assert result.evidence.protocol_id == "example.protocol"
    assert result.after_state["input"] == {"operation": "operational-observation"}
    assert result.observation["snapshot"] == result.after_state
    assert len(result.observation["evidence_lineage"]) == 1

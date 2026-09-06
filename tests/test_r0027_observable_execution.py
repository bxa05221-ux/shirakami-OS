from runtime.adapter import adapt_landscape_observation
from runtime.landscape import LandscapeState
from runtime.landscape_execution import execute_on_landscape
from runtime.observable_execution import execute_observably
from runtime.prototype import Runtime, example_protocol


def test_r0027_exposes_before_evidence_after_and_reobservation():
    state = LandscapeState.from_snapshot(
        {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}
    )
    result = execute_observably(
        state,
        Runtime(),
        "example.protocol",
        example_protocol,
        {"message": "hello landscape"},
    )

    assert result.before_state == {
        "repository": "bxa05221-ux/shirakami-OS",
        "branch": "main",
    }
    assert result.evidence.protocol_id == "example.protocol"
    assert result.evidence.transition_kind == "example.transition"
    assert result.after_state["input"] == {"message": "hello landscape"}
    assert result.after_state["changed"] is True
    assert result.observation["snapshot"] == result.after_state
    assert len(result.observation["evidence_lineage"]) == 1
    assert result.observation["evidence_lineage"][0]["protocol_id"] == "example.protocol"
    assert set(result.observation) == {"snapshot", "evidence_lineage"}

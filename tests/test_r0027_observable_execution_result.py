from runtime.landscape import LandscapeState
from runtime.observable_execution import execute_observable
from runtime.prototype import Runtime, example_protocol


def test_execute_observable_exposes_before_evidence_after_and_observation():
    state = LandscapeState.from_snapshot(
        {"repository": "bxa05221-ux/shirakami-OS", "branch": "main"}
    )

    result = execute_observable(
        state,
        Runtime(),
        "example.protocol",
        example_protocol,
        {"message": "hello landscape"},
    )

    assert result.before == {
        "repository": "bxa05221-ux/shirakami-OS",
        "branch": "main",
    }
    assert result.evidence.protocol_id == "example.protocol"
    assert result.after["input"] == {"message": "hello landscape"}
    assert result.after["changed"] is True
    assert result.observation["snapshot"] == result.after
    assert len(result.observation["evidence_lineage"]) == 1
    assert result.observation["evidence_lineage"][0]["protocol_id"] == "example.protocol"

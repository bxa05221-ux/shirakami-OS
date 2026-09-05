from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.prototype import ExecutionResult, Transition


def _result(protocol_id: str, transition_id: str, source: str, result: str) -> ExecutionResult:
    return ExecutionResult(
        status="completed",
        protocol_id=protocol_id,
        transition=Transition(
            kind="r0014.landscape.transition",
            data={
                "protocol_id": protocol_id,
                "transition_id": transition_id,
                "source_landscape_state": source,
                "resulting_landscape_state": result,
                "changed": True,
            },
        ),
    )


def test_accumulated_evidence_is_observable_as_final_landscape_state():
    transitions = [
        _result("r0014.landscape.v1", "transition-r0014-001", "landscape-r0014-001", "landscape-r0014-002"),
        _result("r0014.landscape.v2", "transition-r0014-002", "landscape-r0014-002", "landscape-r0014-003"),
        _result("r0014.landscape.v3", "transition-r0014-003", "landscape-r0014-003", "landscape-r0014-004"),
    ]

    state = LandscapeState.empty()
    for result in transitions:
        state.apply_evidence(capture_evidence(result))

    snapshot = state.snapshot()

    assert len(state.evidence) == 3
    assert snapshot["protocol_id"] == "r0014.landscape.v3"
    assert snapshot["transition_id"] == "transition-r0014-003"
    assert snapshot["source_landscape_state"] == "landscape-r0014-003"
    assert snapshot["resulting_landscape_state"] == "landscape-r0014-004"
    assert snapshot["changed"] is True
    assert "continuity" not in snapshot
    assert "continuity_claim" not in snapshot


def test_final_landscape_observation_does_not_erase_evidence_lineage():
    transitions = [
        _result("r0014.landscape.v1", "transition-r0014-001", "landscape-r0014-001", "landscape-r0014-002"),
        _result("r0014.landscape.v2", "transition-r0014-002", "landscape-r0014-002", "landscape-r0014-003"),
        _result("r0014.landscape.v3", "transition-r0014-003", "landscape-r0014-003", "landscape-r0014-004"),
    ]

    state = LandscapeState.empty()
    for result in transitions:
        state.apply_evidence(capture_evidence(result))

    observed_lineage = [
        (item.protocol_id, item.transition_data["transition_id"])
        for item in state.evidence
    ]

    assert observed_lineage == [
        ("r0014.landscape.v1", "transition-r0014-001"),
        ("r0014.landscape.v2", "transition-r0014-002"),
        ("r0014.landscape.v3", "transition-r0014-003"),
    ]

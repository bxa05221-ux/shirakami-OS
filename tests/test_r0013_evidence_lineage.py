from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.prototype import ExecutionResult, Transition


def _result(protocol_id: str, transition_id: str, source: str, result: str) -> ExecutionResult:
    return ExecutionResult(
        status="completed",
        transition=Transition(
            kind="r0013.landscape.transition",
            data={
                "protocol_id": protocol_id,
                "transition_id": transition_id,
                "source_landscape_state": source,
                "resulting_landscape_state": result,
                "changed": True,
            },
        ),
    )


def test_multiple_transitions_preserve_ordered_evidence_lineage():
    transitions = [
        _result("r0013.lineage.v1", "transition-r0013-001", "landscape-r0013-001", "landscape-r0013-002"),
        _result("r0013.lineage.v2", "transition-r0013-002", "landscape-r0013-002", "landscape-r0013-003"),
        _result("r0013.lineage.v3", "transition-r0013-003", "landscape-r0013-003", "landscape-r0013-004"),
    ]

    evidence = [capture_evidence(result, protocol_id=result.transition.data["protocol_id"]) for result in transitions]

    assert [item.transition_data["transition_id"] for item in evidence] == [
        "transition-r0013-001",
        "transition-r0013-002",
        "transition-r0013-003",
    ]
    assert [item.protocol_id for item in evidence] == [
        "r0013.lineage.v1",
        "r0013.lineage.v2",
        "r0013.lineage.v3",
    ]
    assert all("continuity" not in item.transition_data for item in evidence)


def test_multiple_evidence_records_project_in_order_without_continuity_claim():
    transitions = [
        _result("r0013.lineage.v1", "transition-r0013-001", "landscape-r0013-001", "landscape-r0013-002"),
        _result("r0013.lineage.v2", "transition-r0013-002", "landscape-r0013-002", "landscape-r0013-003"),
        _result("r0013.lineage.v3", "transition-r0013-003", "landscape-r0013-003", "landscape-r0013-004"),
    ]

    state = LandscapeState.empty()
    for result in transitions:
        evidence = capture_evidence(result, protocol_id=result.transition.data["protocol_id"])
        state.apply_evidence(evidence)

    snapshot = state.snapshot()
    assert snapshot["protocol_id"] == "r0013.lineage.v3"
    assert snapshot["transition_id"] == "transition-r0013-003"
    assert snapshot["source_landscape_state"] == "landscape-r0013-003"
    assert snapshot["resulting_landscape_state"] == "landscape-r0013-004"
    assert [item.transition_data["transition_id"] for item in state.evidence] == [
        "transition-r0013-001",
        "transition-r0013-002",
        "transition-r0013-003",
    ]
    assert "continuity" not in snapshot

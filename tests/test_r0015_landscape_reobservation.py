from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.prototype import ExecutionResult, Transition


def _result(protocol_id: str, transition_id: str, source: str, resulting: str) -> ExecutionResult:
    return ExecutionResult(
        status="completed",
        protocol_id=protocol_id,
        transition=Transition(
            kind="r0015.landscape.transition",
            data={
                "protocol_id": protocol_id,
                "transition_id": transition_id,
                "source_landscape_state": source,
                "resulting_landscape_state": resulting,
                "changed": True,
            },
        ),
    )


def test_same_evidence_sequence_reproduces_same_landscape_snapshot():
    results = [
        _result("r0015.lineage.v1", "transition-r0015-001", "landscape-r0015-001", "landscape-r0015-002"),
        _result("r0015.lineage.v2", "transition-r0015-002", "landscape-r0015-002", "landscape-r0015-003"),
        _result("r0015.lineage.v3", "transition-r0015-003", "landscape-r0015-003", "landscape-r0015-004"),
    ]
    evidence = [capture_evidence(result) for result in results]

    first = LandscapeState.empty()
    second = LandscapeState.empty()
    for record in evidence:
        first.apply_evidence(record)
        second.apply_evidence(record)

    assert first.snapshot() == second.snapshot()
    assert [record.transition_data["transition_id"] for record in first.evidence] == [
        "transition-r0015-001",
        "transition-r0015-002",
        "transition-r0015-003",
    ]
    assert [record.transition_data["transition_id"] for record in second.evidence] == [
        "transition-r0015-001",
        "transition-r0015-002",
        "transition-r0015-003",
    ]
    assert "continuity" not in first.snapshot()
    assert "continuity_claim" not in first.snapshot()


def test_reobservation_does_not_create_semantic_continuity_claim():
    result = _result(
        "r0015.lineage.v1",
        "transition-r0015-001",
        "landscape-r0015-001",
        "landscape-r0015-002",
    )
    evidence = capture_evidence(result)

    state = LandscapeState.empty()
    state.apply_evidence(evidence)

    assert state.snapshot()["source_landscape_state"] == "landscape-r0015-001"
    assert state.snapshot()["resulting_landscape_state"] == "landscape-r0015-002"
    assert "continuity" not in state.snapshot()
    assert "continuity_claim" not in state.snapshot()

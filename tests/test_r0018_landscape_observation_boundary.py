from evidence import capture_evidence
from landscape import LandscapeState
from prototype import ExecutionResult, Transition


def _result(protocol_id: str, transition_id: str, resulting_state: str) -> ExecutionResult:
    return ExecutionResult(
        status="completed",
        protocol_id=protocol_id,
        transition=Transition(
            kind="r0018.landscape.transition",
            data={
                "protocol_id": protocol_id,
                "transition_id": transition_id,
                "source_landscape_state": "landscape-r0018-source",
                "resulting_landscape_state": resulting_state,
                "changed": True,
            },
        ),
    )


def test_landscape_snapshot_is_plain_observable_state():
    state = LandscapeState.empty()
    evidence = capture_evidence(_result("r0018.v1", "transition-r0018-001", "landscape-r0018-001"))
    state.apply_evidence(evidence)
    snapshot = state.snapshot()
    assert snapshot["protocol_id"] == "r0018.v1"
    assert snapshot["transition_id"] == "transition-r0018-001"
    assert snapshot["resulting_landscape_state"] == "landscape-r0018-001"
    assert "evidence" not in snapshot
    assert "continuity" not in snapshot
    assert "continuity_claim" not in snapshot


def test_observation_does_not_mutate_evidence_lineage():
    state = LandscapeState.empty()
    evidence = [
        capture_evidence(_result("r0018.v1", "transition-r0018-001", "landscape-r0018-001")),
        capture_evidence(_result("r0018.v2", "transition-r0018-002", "landscape-r0018-002")),
    ]
    for record in evidence:
        state.apply_evidence(record)
    before = [(e.protocol_id, e.transition_data["transition_id"]) for e in state.evidence]
    _ = state.snapshot()
    after = [(e.protocol_id, e.transition_data["transition_id"]) for e in state.evidence]
    assert before == after
    assert len(state.evidence) == 2

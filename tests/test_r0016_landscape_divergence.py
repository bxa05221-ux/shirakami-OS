from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.prototype import ExecutionResult, Transition


def _result(protocol_id: str, transition_id: str, source: str, resulting: str) -> ExecutionResult:
    return ExecutionResult(
        status="completed",
        protocol_id=protocol_id,
        transition=Transition(
            kind="r0016.landscape.transition",
            data={
                "protocol_id": protocol_id,
                "transition_id": transition_id,
                "source_landscape_state": source,
                "resulting_landscape_state": resulting,
                "changed": True,
            },
        ),
    )


def _project(results: list[ExecutionResult]) -> LandscapeState:
    state = LandscapeState.empty()
    for result in results:
        state.apply_evidence(capture_evidence(result))
    return state


def test_different_evidence_is_observable_as_different_landscape():
    common = [
        _result("r0016.lineage.v1", "transition-r0016-001", "landscape-r0016-001", "landscape-r0016-002"),
        _result("r0016.lineage.v2", "transition-r0016-002", "landscape-r0016-002", "landscape-r0016-003"),
    ]
    left = common + [
        _result("r0016.lineage.v3", "transition-r0016-003-left", "landscape-r0016-003", "landscape-r0016-004-left"),
    ]
    right = common + [
        _result("r0016.lineage.v3", "transition-r0016-003-right", "landscape-r0016-003", "landscape-r0016-004-right"),
    ]

    left_state = _project(left)
    right_state = _project(right)

    assert left_state.snapshot() != right_state.snapshot()
    assert left_state.snapshot()["transition_id"] != right_state.snapshot()["transition_id"]
    assert left_state.snapshot()["resulting_landscape_state"] != right_state.snapshot()["resulting_landscape_state"]
    assert "continuity" not in left_state.snapshot()
    assert "continuity_claim" not in left_state.snapshot()
    assert "continuity" not in right_state.snapshot()
    assert "continuity_claim" not in right_state.snapshot()


def test_observable_divergence_does_not_become_semantic_discontinuity_claim():
    left = _project([
        _result("r0016.lineage.v1", "transition-r0016-left", "landscape-r0016-001", "landscape-r0016-left"),
    ])
    right = _project([
        _result("r0016.lineage.v1", "transition-r0016-right", "landscape-r0016-001", "landscape-r0016-right"),
    ])

    assert left.snapshot() != right.snapshot()
    assert "discontinuity" not in left.snapshot()
    assert "discontinuity" not in right.snapshot()

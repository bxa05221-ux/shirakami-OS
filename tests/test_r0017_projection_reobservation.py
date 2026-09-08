from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.projection import project_evidence
from runtime.prototype import ExecutionResult, Transition


def _result(version: str, transition_id: str, source: str, resulting: str) -> ExecutionResult:
    return ExecutionResult(
        status="completed",
        protocol_id=f"r0017.projection.v{version}",
        transition=Transition(
            kind="r0017.projection.transition",
            data={
                "protocol_id": f"r0017.projection.v{version}",
                "transition_id": transition_id,
                "source_landscape_state": source,
                "resulting_landscape_state": resulting,
                "changed": True,
            },
        ),
    )


def test_same_evidence_sequence_via_projection_produces_same_snapshot():
    results = [
        _result("1", "transition-r0017-001", "landscape-r0017-001", "landscape-r0017-002"),
        _result("2", "transition-r0017-002", "landscape-r0017-002", "landscape-r0017-003"),
        _result("3", "transition-r0017-003", "landscape-r0017-003", "landscape-r0017-004"),
    ]
    evidence = [capture_evidence(result) for result in results]

    first = LandscapeState.empty()
    second = LandscapeState.empty()

    for record in evidence:
        project_evidence(record, first)
        project_evidence(record, second)

    assert first.snapshot() == second.snapshot()
    assert [record.transition_data["transition_id"] for record in first.evidence] == [
        "transition-r0017-001",
        "transition-r0017-002",
        "transition-r0017-003",
    ]
    assert [record.transition_data["transition_id"] for record in second.evidence] == [
        "transition-r0017-001",
        "transition-r0017-002",
        "transition-r0017-003",
    ]
    assert "continuity" not in first.snapshot()
    assert "continuity_claim" not in first.snapshot()


def test_projection_does_not_add_semantic_continuity_fields():
    result = _result(
        "1",
        "transition-r0017-001",
        "landscape-r0017-001",
        "landscape-r0017-002",
    )
    evidence = capture_evidence(result)
    state = LandscapeState.empty()

    projected = project_evidence(evidence, state)

    assert projected["protocol_id"] == "r0017.projection.v1"
    assert projected["transition_id"] == "transition-r0017-001"
    assert projected["source_landscape_state"] == "landscape-r0017-001"
    assert projected["resulting_landscape_state"] == "landscape-r0017-002"
    assert "continuity" not in projected
    assert "continuity_claim" not in projected

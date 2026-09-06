from runtime.adapter import adapt_landscape_observation
from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.prototype import ExecutionResult, Transition


def _result(protocol_id: str, transition_id: str, source: str, resulting: str):
    return ExecutionResult(
        status="completed",
        protocol_id=protocol_id,
        transition=Transition(
            kind="r0019.landscape.transition",
            data={
                "protocol_id": protocol_id,
                "transition_id": transition_id,
                "source_landscape_state": source,
                "resulting_landscape_state": resulting,
                "changed": True,
            },
        ),
    )


def test_adapter_exposes_snapshot_and_ordered_evidence_lineage():
    results = [
        _result("r0019.v1", "t1", "l0", "l1"),
        _result("r0019.v2", "t2", "l1", "l2"),
        _result("r0019.v3", "t3", "l2", "l3"),
    ]

    state = LandscapeState.empty()
    for result in results:
        state.apply_evidence(capture_evidence(result))

    observation = adapt_landscape_observation(state)

    assert observation["snapshot"]["protocol_id"] == "r0019.v3"
    assert observation["snapshot"]["transition_id"] == "t3"
    assert observation["snapshot"]["resulting_landscape_state"] == "l3"
    assert [item["transition_data"]["transition_id"] for item in observation["evidence_lineage"]] == ["t1", "t2", "t3"]
    assert [item["protocol_id"] for item in observation["evidence_lineage"]] == ["r0019.v1", "r0019.v2", "r0019.v3"]
    assert "continuity" not in observation
    assert "continuity_claim" not in observation


def test_adapter_does_not_infer_semantic_meaning():
    state = LandscapeState.empty()
    state.apply_evidence(capture_evidence(_result("r0019.v1", "t1", "l0", "l1")))

    observation = adapt_landscape_observation(state)

    assert set(observation) == {"snapshot", "evidence_lineage"}
    assert observation["evidence_lineage"][0]["transition_kind"] == "r0019.landscape.transition"

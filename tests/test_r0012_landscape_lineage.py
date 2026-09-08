from pathlib import Path

from runtime.evidence import capture_evidence
from runtime.landscape import LandscapeState
from runtime.projection import project_evidence
from runtime.prototype import Runtime, Transition


ROOT = Path(__file__).resolve().parents[1]


def test_r0012_evidence_projection_preserves_lineage_as_data():
    runtime = Runtime()

    def protocol(context):
        return Transition(
            kind="r0012.landscape.transition",
            data={
                "transition_id": "transition-r0012-001",
                "source_landscape_state": "landscape-r0012-001",
                "resulting_landscape_state": "landscape-r0012-002",
                "protocol_id": context.protocol_id,
                "changed": True,
            },
        )

    execution = runtime.execute(
        "r0012.lineage.v1",
        protocol,
        {"source_landscape_state": "landscape-r0012-001"},
    )
    evidence = capture_evidence(execution)
    state = LandscapeState.empty()
    projected = project_evidence(evidence, state)

    assert evidence.protocol_id == "r0012.lineage.v1"
    assert evidence.transition_data["transition_id"] == "transition-r0012-001"
    assert evidence.transition_data["source_landscape_state"] == "landscape-r0012-001"
    assert evidence.transition_data["resulting_landscape_state"] == "landscape-r0012-002"
    assert projected["source_landscape_state"] == "landscape-r0012-001"
    assert projected["resulting_landscape_state"] == "landscape-r0012-002"
    assert len(state.evidence) == 1


def test_r0012_projection_does_not_create_continuity_claim():
    runtime = Runtime()

    def protocol(context):
        return Transition(
            kind="r0012.landscape.transition",
            data={
                "source_landscape_state": "landscape-r0012-001",
                "resulting_landscape_state": "landscape-r0012-002",
                "changed": True,
            },
        )

    execution = runtime.execute("r0012.lineage.v1", protocol, {})
    evidence = capture_evidence(execution)
    projected = project_evidence(evidence)

    assert "continuity" not in projected
    assert "continuity_claim" not in projected

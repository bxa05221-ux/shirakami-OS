"""Verification experiments for Evidence crystal/catalyst behavior."""

from evidence import EvidenceRecord
from landscape import LandscapeState


def make_evidence():
    return EvidenceRecord(
        protocol_id="experiment",
        status="success",
        transition_kind="state_change",
        transition_data={"changed": True, "anchor": "X"},
        signals=("observed",),
    )


def test_evidence_crystal_behavior_preserves_identity_across_projections():
    evidence = make_evidence()
    projection_a = LandscapeState.empty()
    projection_b = LandscapeState.empty()

    projection_a.apply_evidence(evidence)
    projection_b.apply_evidence(evidence)

    assert evidence.protocol_id == "experiment"
    assert evidence.transition_data["anchor"] == "X"
    assert projection_a.snapshot() == projection_b.snapshot()
    assert projection_a.snapshot()["anchor"] == "X"


def test_evidence_catalyst_behavior_is_non_consuming():
    evidence = make_evidence()
    before = evidence
    consumer_a = LandscapeState.empty()
    consumer_b = LandscapeState.empty()

    consumer_a.apply_evidence(evidence)
    consumer_b.apply_evidence(evidence)

    assert evidence is before
    assert evidence.transition_data["anchor"] == "X"
    assert consumer_a.snapshot()["anchor"] == "X"
    assert consumer_b.snapshot()["anchor"] == "X"


def test_evidence_remains_immutable_while_projection_changes():
    evidence = make_evidence()
    landscape = LandscapeState.empty()

    landscape.apply_evidence(evidence)
    first_projection = landscape.snapshot()

    landscape._state["anchor"] = "Y"
    second_projection = landscape.snapshot()

    assert first_projection["anchor"] == "X"
    assert second_projection["anchor"] == "Y"
    assert evidence.transition_data["anchor"] == "X"

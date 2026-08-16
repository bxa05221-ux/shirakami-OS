from types import MappingProxyType

import pytest

from evidence import EvidenceRecord
from landscape import LandscapeState
from projection import ProjectionError, project_evidence


def make_evidence(protocol_id="example.protocol", changed=True, value="first"):
    return EvidenceRecord(
        protocol_id=protocol_id,
        status="completed",
        transition_kind="example.transition",
        transition_data=MappingProxyType({"changed": changed, "value": value}),
        signals=("execution.completed", "transition.observed"),
    )


def test_projection_is_separate_from_evidence_and_state():
    evidence = make_evidence()
    original = dict(evidence.transition_data)
    landscape = LandscapeState.empty()

    projection = project_evidence(evidence)

    assert dict(evidence.transition_data) == original
    assert landscape.snapshot() == {}
    assert projection.changes["value"] == "first"

    landscape.apply_projection(projection)

    assert landscape.snapshot()["value"] == "first"
    assert landscape.projection_history() == (projection,)
    assert dict(evidence.transition_data) == original


def test_apply_evidence_uses_projection_boundary():
    evidence = make_evidence(value="projected")
    landscape = LandscapeState.empty()

    landscape.apply_evidence(evidence)

    history = landscape.projection_history()
    assert landscape.snapshot()["value"] == "projected"
    assert len(history) == 1
    assert history[0].evidence_id == "example.protocol:completed:example.transition"
    assert dict(evidence.transition_data)["value"] == "projected"


def test_non_transition_evidence_is_not_projected():
    evidence = make_evidence(changed=False)
    landscape = LandscapeState.empty()

    with pytest.raises(ProjectionError):
        project_evidence(evidence)

    landscape.apply_evidence(evidence)
    assert landscape.snapshot() == {}
    assert landscape.projection_history() == ()


def test_reobservation_preserves_previous_projection():
    evidence1 = make_evidence(value="first")
    landscape = LandscapeState.empty()
    projection1 = project_evidence(evidence1)
    landscape.apply_projection(projection1)

    # Re-observation produces a distinct EvidenceRecord; Evidence1 remains
    # immutable and its projection remains in the history.
    evidence2 = make_evidence(value="second")
    projection2 = project_evidence(evidence2)
    landscape.apply_projection(projection2)

    history = landscape.projection_history()
    assert len(history) == 2
    assert history[0] is projection1
    assert history[1] is projection2
    assert history[0].changes["value"] == "first"
    assert history[1].changes["value"] == "second"
    assert dict(evidence1.transition_data)["value"] == "first"
    assert dict(evidence2.transition_data)["value"] == "second"
    assert landscape.snapshot()["value"] == "second"

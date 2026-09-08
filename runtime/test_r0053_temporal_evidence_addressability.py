from evidence import EvidenceRecord
from landscape import LandscapeState


def test_r0053_temporal_evidence_addressability():
    evidence_a = EvidenceRecord(
        protocol_id="r0053",
        status="success",
        transition_kind="update",
        transition_data={"changed": True, "value": "A"},
        signals=("t1",),
    )
    evidence_b = EvidenceRecord(
        protocol_id="r0053",
        status="success",
        transition_kind="update",
        transition_data={"changed": True, "value": "B"},
        signals=("t2",),
    )

    state = LandscapeState.empty()
    state.apply_evidence(evidence_a)
    state.apply_evidence(evidence_b)

    assert state.evidence == [evidence_a, evidence_b]
    assert state.evidence[0] is evidence_a
    assert state.evidence[1] is evidence_b
    assert state.evidence[0].transition_data["value"] == "A"
    assert state.evidence[1].transition_data["value"] == "B"
    assert [record.signals[0] for record in state.evidence] == ["t1", "t2"]
    assert state.snapshot()["value"] == "B"

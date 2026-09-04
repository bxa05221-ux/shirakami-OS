from evidence import EvidenceRecord
from landscape import LandscapeState


def test_failed_transition_does_not_propagate_to_landscape():
    success = EvidenceRecord(
        protocol_id="p1",
        status="success",
        transition_kind="update",
        transition_data={"changed": True, "value": "kept"},
        signals=("s1",),
    )
    failed = EvidenceRecord(
        protocol_id="p1",
        status="failed",
        transition_kind="update",
        transition_data={"changed": False, "value": "must-not-propagate"},
        signals=("s2",),
    )

    state = LandscapeState.empty()
    state.apply_evidence(success)
    before = state.snapshot()

    state.apply_evidence(failed)

    assert state.snapshot() == before
    assert state.evidence == [success]

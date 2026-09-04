from evidence import EvidenceRecord
from landscape import LandscapeState
from replay import landscape_fingerprint, replay_landscape


def test_evidence_replay_reconstructs_identical_landscape():
    evidence = [
        EvidenceRecord(
            protocol_id="p1",
            status="success",
            transition_kind="update",
            transition_data={"changed": True, "value": "first"},
            signals=("s1",),
        ),
        EvidenceRecord(
            protocol_id="p1",
            status="success",
            transition_kind="update",
            transition_data={"changed": True, "value": "second"},
            signals=("s2",),
        ),
    ]

    projected = LandscapeState.empty()
    for record in evidence:
        projected.apply_evidence(record)

    replayed = replay_landscape(evidence)

    assert replayed == projected.snapshot()
    assert landscape_fingerprint(replayed) == landscape_fingerprint(projected.snapshot())

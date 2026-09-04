from evidence import EvidenceRecord
from landscape import LandscapeState
from replay import landscape_fingerprint, replay_landscape


def make_evidence(key, value):
    return EvidenceRecord(
        protocol_id="determinism-test",
        status="success",
        transition_kind="update",
        transition_data={key: value, "changed": True},
        signals=(f"{key}={value}",),
    )


def test_same_evidence_sequence_reconstructs_identical_landscape():
    records = (
        make_evidence("stage", "one"),
        make_evidence("stage", "two"),
        make_evidence("status", "stable"),
    )
    first = replay_landscape(records)
    second = replay_landscape(records)
    assert first == second
    assert landscape_fingerprint(first) == landscape_fingerprint(second)


def test_projection_matches_replay_for_same_evidence_sequence():
    records = (
        make_evidence("mode", "observe"),
        make_evidence("mode", "project"),
        make_evidence("result", "complete"),
    )
    projected = LandscapeState.empty()
    for record in records:
        projected.apply_evidence(record)
    replayed = replay_landscape(records)
    assert projected.snapshot() == replayed
    assert landscape_fingerprint(projected.snapshot()) == landscape_fingerprint(replayed)

from evidence import EvidenceRecord
from landscape import LandscapeState
from replay import landscape_fingerprint, replay_landscape


def _evidence(key, value):
    return EvidenceRecord(
        protocol_id="determinism-test",
        status="success",
        transition_kind="update",
        transition_data={key: value, "changed": True},
        signals=(f"{key}={value}",),
    )


def test_same_evidence_sequence_reconstructs_identical_landscape():
    records = (
        _evidence("stage", "one"),
        _evidence("stage", "two"),
        _evidence("status", "stable"),
    )

    first = replay_landscape(records)
    second = replay_landscape(records)

    assert first == second
    assert landscape_fingerprint(first) == landscape_fingerprint(second)


def test_projection_and_replay_are_deterministic_for_same_evidence_sequence():
    records = (
        _evidence("mode", "observe"),
        _evidence("mode", "project"),
        _evidence("result", "complete"),
    )

    projected = LandscapeState.empty()
    for record in records:
        projected.apply_evidence(record)

    replayed = replay_landscape(records)

    assert projected.snapshot() == replayed
    assert landscape_fingerprint(projected.snapshot()) == landscape_fingerprint(replayed)

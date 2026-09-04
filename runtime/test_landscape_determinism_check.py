from evidence import EvidenceRecord
from landscape import LandscapeState
from replay import landscape_fingerprint, replay_landscape


def make_evidence(key, value):
    return EvidenceRecord("determinism-test", "success", "update", {key: value, "changed": True}, (f"{key}={value}",))


def test_replay_is_deterministic():
    records = (make_evidence("stage", "one"), make_evidence("stage", "two"), make_evidence("status", "stable"))
    first = replay_landscape(records)
    second = replay_landscape(records)
    assert first == second
    assert landscape_fingerprint(first) == landscape_fingerprint(second)


def test_projection_matches_replay():
    records = (make_evidence("mode", "observe"), make_evidence("mode", "project"), make_evidence("result", "complete"))
    projected = LandscapeState.empty()
    for record in records:
        projected.apply_evidence(record)
    assert projected.snapshot() == replay_landscape(records)

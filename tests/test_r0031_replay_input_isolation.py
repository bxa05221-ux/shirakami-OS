from runtime.evidence import capture_evidence
from runtime.evidence_replay import replay_evidence
from runtime.replay_observation import replay_snapshot
from runtime.prototype import Runtime, example_protocol


def _records():
    runtime = Runtime()
    records = []
    for value in ("one", "two", "three"):
        records.append(capture_evidence(runtime.execute("example.protocol", example_protocol, {"value": value})))
    return records


def test_replay_snapshot_does_not_mutate_evidence_input():
    records = _records()
    before = list(records)
    snapshot = replay_snapshot(records)

    assert snapshot == replay_evidence(records).snapshot()
    assert records == before


def test_replay_snapshot_returns_observable_state_only():
    snapshot = replay_snapshot(_records())

    assert set(snapshot) == {"protocol_id", "input", "changed"}
    assert "evidence" not in snapshot
    assert "continuity" not in snapshot
    assert "identity" not in snapshot

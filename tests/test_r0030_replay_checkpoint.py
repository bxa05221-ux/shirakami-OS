from runtime.evidence import capture_evidence
from runtime.evidence_checkpoint import replay_evidence_from_snapshot
from runtime.evidence_replay import replay_evidence
from runtime.landscape import LandscapeState
from runtime.prototype import Runtime, example_protocol


def _evidence_sequence():
    runtime = Runtime()
    source = LandscapeState.empty()
    records = []
    for value in ("one", "two", "three", "four"):
        result = runtime.execute("example.protocol", example_protocol, {"value": value})
        record = capture_evidence(result)
        source.apply_evidence(record)
        records.append(record)
    return source, records


def test_checkpoint_plus_tail_reconstructs_same_observable_state():
    source, records = _evidence_sequence()
    checkpoint = replay_evidence(records[:2])

    reconstructed = replay_evidence_from_snapshot(
        checkpoint.snapshot(), records[2:]
    )

    assert reconstructed.snapshot() == source.snapshot()
    assert reconstructed.evidence == records[2:]


def test_checkpoint_replay_keeps_checkpoint_history_out_of_local_evidence():
    _, records = _evidence_sequence()
    checkpoint = replay_evidence(records[:2])

    reconstructed = replay_evidence_from_snapshot(
        checkpoint.snapshot(), records[2:]
    )

    assert [
        item.transition_data["input"]["value"] for item in reconstructed.evidence
    ] == ["three", "four"]

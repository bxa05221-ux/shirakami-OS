from runtime.evidence import capture_evidence
from runtime.evidence_replay import replay_evidence
from runtime.landscape import LandscapeState
from runtime.prototype import Runtime, example_protocol


def _evidence_sequence():
    runtime = Runtime()
    source = LandscapeState.empty()
    records = []
    for value in ("one", "two", "three"):
        result = runtime.execute("example.protocol", example_protocol, {"value": value})
        record = capture_evidence(result)
        source.apply_evidence(record)
        records.append(record)
    return source, records


def test_replay_reconstructs_observable_snapshot_in_order():
    source, records = _evidence_sequence()

    reconstructed = replay_evidence(records)

    assert reconstructed.snapshot() == source.snapshot()
    assert reconstructed.evidence == records
    assert [item.transition_data["input"]["value"] for item in reconstructed.evidence] == [
        "one",
        "two",
        "three",
    ]


def test_replay_does_not_claim_continuity_or_identity():
    _, records = _evidence_sequence()

    reconstructed = replay_evidence(records)

    assert set(reconstructed.snapshot()) == {"protocol_id", "input", "changed"}
    assert not any("continuity" in key or "identity" in key for key in reconstructed.snapshot())

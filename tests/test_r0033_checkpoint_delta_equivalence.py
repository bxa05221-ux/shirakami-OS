from runtime.checkpoint_delta_equivalence import equivalent_observable_state, replay_checkpoint_with_delta
from runtime.evidence import EvidenceRecord
from runtime.evidence_replay import replay_evidence


def record(value: str) -> EvidenceRecord:
    return EvidenceRecord(
        protocol_id="example.protocol",
        status="success",
        transition_kind="example.transition",
        transition_data={"value": value, "changed": True},
        signals=(),
    )


def test_checkpoint_plus_delta_matches_full_replay() -> None:
    one, two, three = record("one"), record("two"), record("three")
    records = [one, two, three]
    applied = [one, two]
    checkpoint = replay_evidence(applied).snapshot()

    reconstructed = replay_checkpoint_with_delta(checkpoint, records, applied)
    full = replay_evidence(records)

    assert reconstructed.snapshot() == full.snapshot()
    assert equivalent_observable_state(records, checkpoint, applied)
    assert reconstructed.snapshot()["value"] == "three"


def test_checkpoint_plus_delta_does_not_mutate_inputs() -> None:
    one, two, three = record("one"), record("two"), record("three")
    records = [one, two, three]
    applied = [one, two]
    checkpoint = replay_evidence(applied).snapshot()

    replay_checkpoint_with_delta(checkpoint, records, applied)

    assert records == [one, two, three]
    assert applied == [one, two]
    assert checkpoint == replay_evidence(applied).snapshot()

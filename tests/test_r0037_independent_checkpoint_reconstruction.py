from runtime.adapter import MemoryAdapter
from runtime.evidence import capture_evidence
from runtime.independent_checkpoint_reobservation import compare_reconstructed_checkpoint
from runtime.prototype import ExecutionResult, Transition


def record(key, value):
    return capture_evidence(
        ExecutionResult(
            status="completed",
            protocol_id="example.protocol",
            transition=Transition(
                kind="matome.protocol.transition",
                data={key: value, "changed": True},
            ),
        )
    )


def test_independent_checkpoint_reconstruction_preserves_snapshot_equivalence():
    first = record("first", 1)
    second = record("second", 2)
    third = record("third", 3)
    records = [first, second, third]
    applied = [first, second]
    snapshot = {"first": 1, "second": 2, "changed": True}

    result = compare_reconstructed_checkpoint(
        snapshot,
        records,
        applied,
        MemoryAdapter(),
    )

    assert result["equivalent"] is False
    assert result["full"]["snapshot"] == result["reconstructed"]["snapshot"]
    assert result["full"]["evidence_lineage"] != result["reconstructed"]["evidence_lineage"]
    assert snapshot == {"first": 1, "second": 2, "changed": True}
    assert records == [first, second, third]
    assert applied == [first, second]

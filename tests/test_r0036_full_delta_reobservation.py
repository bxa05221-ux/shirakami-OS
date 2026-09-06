from runtime.adapter import MemoryAdapter
from runtime.evidence import capture_evidence
from runtime.full_delta_reobservation import compare_full_and_delta_reobservation
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


def test_full_and_delta_reobservation_separate_snapshot_and_lineage():
    first = record("first", 1)
    second = record("second", 2)
    third = record("third", 3)
    records = [first, second, third]
    applied = [first, second]

    result = compare_full_and_delta_reobservation(
        {"first": 1, "second": 2, "changed": True},
        records,
        applied,
        MemoryAdapter(),
    )

    assert result["snapshot_equivalent"] is True
    assert result["lineage_equivalent"] is False
    assert result["full"]["snapshot"] == result["delta"]["snapshot"]
    assert result["full"]["evidence_lineage"] != result["delta"]["evidence_lineage"]
    assert records == [first, second, third]
    assert applied == [first, second]

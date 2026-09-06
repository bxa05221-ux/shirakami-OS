from runtime.evidence import EvidenceRecord
from runtime.protocol_version_replay import (
    protocol_version_from_evidence,
    replay_with_historical_protocol_versions,
)


def record(protocol_id: str, version: str, key: str, value: object) -> EvidenceRecord:
    return EvidenceRecord(
        protocol_id=protocol_id,
        status="prepared",
        transition_kind="matome.protocol.transition",
        transition_data={
            "protocol_id": protocol_id,
            "protocol_version": version,
            key: value,
            "changed": True,
        },
        signals=(),
    )


def test_historical_protocol_version_is_read_from_evidence():
    evidence = record("matome.protocol", "0.1", "first", 1)

    assert protocol_version_from_evidence(evidence) == "0.1"


def test_replay_preserves_historical_version_when_current_version_differs():
    first = record("matome.protocol", "0.1", "first", 1)
    second = record("matome.protocol", "0.2", "second", 2)

    result = replay_with_historical_protocol_versions(
        [first, second],
        {"matome.protocol": "0.3"},
    )

    assert result["snapshot"] == {
        "protocol_id": "matome.protocol",
        "protocol_version": "0.2",
        "second": 2,
        "changed": True,
    }
    assert result["protocol_version_lineage"] == (
        {
            "protocol_id": "matome.protocol",
            "historical_version": "0.1",
            "current_version": "0.3",
        },
        {
            "protocol_id": "matome.protocol",
            "historical_version": "0.2",
            "current_version": "0.3",
        },
    )
    assert result["protocol_version_lineage"][0]["historical_version"] != result["protocol_version_lineage"][0]["current_version"]

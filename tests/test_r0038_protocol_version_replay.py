from runtime.evidence import capture_evidence
from runtime.protocol_version_replay import (
    protocol_version_from_evidence,
    replay_with_historical_protocol_versions,
)
from runtime.prototype import ExecutionResult, Transition


def record(protocol_id, version, key, value):
    return capture_evidence(
        ExecutionResult(
            status="completed",
            protocol_id=protocol_id,
            transition=Transition(
                kind="matome.protocol.transition",
                data={
                    "protocol_id": protocol_id,
                    "protocol_version": version,
                    key: value,
                    "changed": True,
                },
            ),
        )
    )


def test_replay_uses_historical_version_carried_by_evidence():
    first = record("example.protocol", "1.0", "first", 1)
    second = record("example.protocol", "1.1", "second", 2)

    result = replay_with_historical_protocol_versions(
        [first, second],
        {"example.protocol": "2.0"},
    )

    assert protocol_version_from_evidence(first) == "1.0"
    assert protocol_version_from_evidence(second) == "1.1"
    assert result["snapshot"] == {
        "protocol_id": "example.protocol",
        "protocol_version": "1.1",
        "first": 1,
        "second": 2,
        "changed": True,
    }
    assert result["protocol_version_lineage"] == (
        {
            "protocol_id": "example.protocol",
            "historical_version": "1.0",
            "current_version": "2.0",
        },
        {
            "protocol_id": "example.protocol",
            "historical_version": "1.1",
            "current_version": "2.0",
        },
    )

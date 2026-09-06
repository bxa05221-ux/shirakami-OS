from runtime.protocol_artifact_hash import hash_protocol_artifact
from runtime.protocol_artifact_mismatch import detect_artifact_mismatch


def test_matching_artifact_hash_is_reported_as_match():
    artifact = b"title: example\nversion: 1\n"
    expected = hash_protocol_artifact(artifact)

    result = detect_artifact_mismatch(expected, artifact)

    assert result["matches"] is True
    assert result["mismatch"] is False
    assert result["expected_hash"] == expected
    assert result["current_hash"] == expected


def test_changed_artifact_is_reported_as_mismatch():
    historical = b"title: example\nversion: 1\n"
    current = b"title: example\nversion: 2\n"
    expected = hash_protocol_artifact(historical)

    result = detect_artifact_mismatch(expected, current)

    assert result["matches"] is False
    assert result["mismatch"] is True
    assert result["expected_hash"] == expected
    assert result["current_hash"] != expected


def test_detection_does_not_mutate_artifact_bytes():
    artifact = b"immutable protocol bytes"
    expected = hash_protocol_artifact(artifact)

    detect_artifact_mismatch(expected, artifact)

    assert artifact == b"immutable protocol bytes"

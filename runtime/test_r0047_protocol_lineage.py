from runtime.protocol_artifact_hash import hash_protocol_artifact, verify_protocol_artifact_hash
from runtime.protocol_artifact_mismatch import detect_artifact_mismatch


def test_same_protocol_identity_can_have_distinct_artifact_identity():
    protocol_id = "lineage.protocol"
    artifact_a = b"title: example\nversion: 1\n"
    artifact_b = b"title: example\nversion: 2\n"

    hash_a = hash_protocol_artifact(artifact_a)
    hash_b = hash_protocol_artifact(artifact_b)

    assert protocol_id == "lineage.protocol"
    assert hash_a != hash_b
    assert verify_protocol_artifact_hash(artifact_a, hash_a)
    assert verify_protocol_artifact_hash(artifact_b, hash_b)


def test_protocol_artifact_mismatch_remains_observable_without_reconciliation():
    protocol_id = "lineage.protocol"
    historical_artifact = b"title: example\nversion: 1\n"
    current_artifact = b"title: example\nversion: 2\n"
    historical_hash = hash_protocol_artifact(historical_artifact)

    observation = detect_artifact_mismatch(historical_hash, current_artifact)

    assert protocol_id == "lineage.protocol"
    assert observation["expected_hash"] == historical_hash
    assert observation["current_hash"] == hash_protocol_artifact(current_artifact)
    assert observation["mismatch"] is True
    assert observation["matches"] is False

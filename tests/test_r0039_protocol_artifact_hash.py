from runtime.protocol_artifact_hash import (
    hash_protocol_artifact,
    verify_protocol_artifact_hash,
)


def test_identical_artifact_bytes_have_identical_hashes():
    artifact = b"matome: protocol\nversion: 0.1\n"
    assert hash_protocol_artifact(artifact) == hash_protocol_artifact(artifact)


def test_changed_artifact_bytes_have_different_hashes():
    original = b"matome: protocol\nversion: 0.1\n"
    changed = b"matome: protocol\nversion: 0.2\n"
    assert hash_protocol_artifact(original) != hash_protocol_artifact(changed)


def test_expected_historical_hash_is_read_only_verifiable():
    artifact = b"historical protocol artifact"
    expected = hash_protocol_artifact(artifact)
    assert verify_protocol_artifact_hash(artifact, expected) is True
    assert verify_protocol_artifact_hash(b"changed artifact", expected) is False


def test_hash_is_hex_sha256_digest():
    artifact = b"artifact"
    digest = hash_protocol_artifact(artifact)
    assert len(digest) == 64
    assert all(character in "0123456789abcdef" for character in digest)

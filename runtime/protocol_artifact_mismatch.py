"""Read-only Protocol artifact hash mismatch detection for Runtime β0.1."""

from collections.abc import Mapping

from .protocol_artifact_hash import hash_protocol_artifact


def detect_artifact_mismatch(
    expected_hash: str,
    artifact: bytes,
) -> Mapping[str, object]:
    """Compare an explicit historical hash with the current artifact bytes."""
    current_hash = hash_protocol_artifact(artifact)
    matches = current_hash == expected_hash
    return {
        "expected_hash": expected_hash,
        "current_hash": current_hash,
        "matches": matches,
        "mismatch": not matches,
    }

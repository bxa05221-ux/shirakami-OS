"""Read-only Protocol artifact hashing boundary for Runtime β0.1."""

from __future__ import annotations

import hashlib


def hash_protocol_artifact(artifact: bytes) -> str:
    """Return the deterministic SHA-256 digest of exact Protocol artifact bytes."""
    return hashlib.sha256(artifact).hexdigest()


def verify_protocol_artifact_hash(artifact: bytes, expected_hash: str) -> bool:
    """Verify exact Protocol artifact bytes against an expected historical hash."""
    return hash_protocol_artifact(artifact) == expected_hash

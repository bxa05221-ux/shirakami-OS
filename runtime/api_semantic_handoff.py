"""Semantic handoff boundary for the external Shirakami observation API."""

from typing import Any

FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {
        "approval",
        "approval_envelope",
        "execution_authorized",
        "human_authorized",
        "activation",
        "execution_id",
    }
)


def validate_semantic_handoff(payload: dict[str, Any]) -> None:
    """Reject authority semantics instead of silently assigning them meaning."""
    forbidden = sorted(FORBIDDEN_AUTHORITY_FIELDS.intersection(payload))
    if forbidden:
        raise ValueError(
            "authority fields are not accepted by /observe: " + ", ".join(forbidden)
        )


def preserve_protocol_reference(payload: dict[str, Any]) -> str | None:
    """Return only an explicitly supplied protocol reference; never infer one."""
    protocol_id = payload.get("protocol_id")
    if protocol_id is None:
        return None
    if not isinstance(protocol_id, str) or not protocol_id:
        raise ValueError("protocol_id must be a non-empty string when supplied")
    return protocol_id

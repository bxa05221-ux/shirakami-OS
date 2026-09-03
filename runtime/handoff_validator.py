"""Sequential Agent handoff boundary validation.

This module validates only the structural contract declared by the
Sequential Verification Multi-Agent Protocol. It does not execute Agents,
repair invalid handoffs, or interpret domain semantics.
"""

from __future__ import annotations

from typing import Any, Mapping


AGENT_BOUNDARIES = {
    "observer": {"facts", "current_state", "detected_gap"},
    "auditor": {"confirmed_boundary", "risk", "minimal_change_candidate"},
    "implementer": {"change", "commit"},
    "verifier": {"pass", "fail", "evidence"},
    "confirmer": {"confirmed", "next_action"},
}

ALLOWED_TRANSITIONS = {
    ("observer", "auditor"),
    ("auditor", "implementer"),
    ("implementer", "verifier"),
    ("verifier", "confirmer"),
    ("confirmer", "observer"),
}

REQUIRED_FIELDS = {
    "state_before",
    "state_after",
    "source_agent",
    "target_agent",
    "payload",
    "allowed_transition",
    "boundary",
}


def validate_handoff(handoff: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one Agent-to-Agent handoff without changing it.

    Returns a stable inspection result. A valid handoff has ``valid=True``;
    invalid input is rejected with explicit reasons. No automatic correction
    is attempted.
    """

    if not isinstance(handoff, Mapping):
        return {"valid": False, "errors": ["handoff must be a mapping"]}

    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(handoff))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    source = handoff.get("source_agent")
    target = handoff.get("target_agent")
    state_before = handoff.get("state_before")
    state_after = handoff.get("state_after")
    payload = handoff.get("payload")
    allowed_transition = handoff.get("allowed_transition")
    boundary = handoff.get("boundary")

    if (source, target) not in ALLOWED_TRANSITIONS:
        errors.append("agent transition is not allowed")

    if state_before != source:
        errors.append("state_before must match source_agent")
    if state_after != target:
        errors.append("state_after must match target_agent")

    if allowed_transition is not True:
        errors.append("allowed_transition must be true")

    if not isinstance(payload, Mapping):
        errors.append("payload must be a mapping")
    else:
        unexpected = sorted(set(payload) - AGENT_BOUNDARIES.get(source, set()))
        if unexpected:
            errors.append(
                f"payload crosses source boundary: {', '.join(unexpected)}"
            )

    if not isinstance(boundary, Mapping):
        errors.append("boundary must be a mapping")
    else:
        if boundary.get("source") != source:
            errors.append("boundary.source must match source_agent")
        if boundary.get("target") != target:
            errors.append("boundary.target must match target_agent")
        if boundary.get("verified") is not True:
            errors.append("boundary.verified must be true")

    return {
        "valid": not errors,
        "errors": tuple(errors),
        "source_agent": source,
        "target_agent": target,
        "state_before": state_before,
        "state_after": state_after,
    }

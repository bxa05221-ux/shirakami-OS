"""Provider-neutral API boundary validation.

This module validates execution context shape and preserves the Human Gate.
Validation describes whether the context is admissible; it never authorizes
execution, publication, or merge.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

REQUIRED_FIELDS = {
    "handoff_id",
    "project",
    "objective",
    "protocol_ids",
    "evidence_ids",
    "verification_scope",
}

FALSE_AUTHORITY_FIELDS = (
    "execution_authorized",
    "publish_authorized",
    "merge_authorized",
)


def validate_execution_context(context: Mapping[str, Any]) -> dict[str, Any]:
    missing = REQUIRED_FIELDS - set(context)
    if missing:
        raise ValueError(f"missing required boundary fields: {sorted(missing)}")

    if not isinstance(context["handoff_id"], str) or not context["handoff_id"].strip():
        raise ValueError("handoff_id must be a non-empty string")
    if not isinstance(context["project"], str) or not context["project"].strip():
        raise ValueError("project must be a non-empty string")
    if not isinstance(context["objective"], str) or not context["objective"].strip():
        raise ValueError("objective must be a non-empty string")
    if not isinstance(context["protocol_ids"], list) or not all(
        isinstance(item, str) and item.strip() for item in context["protocol_ids"]
    ):
        raise ValueError("protocol_ids must be a list of non-empty strings")
    if not isinstance(context["evidence_ids"], list) or not all(
        isinstance(item, str) and item.strip() for item in context["evidence_ids"]
    ):
        raise ValueError("evidence_ids must be a list of non-empty strings")
    if not isinstance(context["verification_scope"], list):
        raise ValueError("verification_scope must be a list")

    for field in FALSE_AUTHORITY_FIELDS:
        if context.get(field, False) is not False:
            raise ValueError(f"{field} must remain false")

    if context.get("human_gate_required", True) is not True:
        raise ValueError("human_gate_required must remain true")

    return {
        "handoff_id": context["handoff_id"],
        "project": context["project"],
        "objective": context["objective"],
        "protocol_ids": list(context["protocol_ids"]),
        "evidence_ids": list(context["evidence_ids"]),
        "verification_scope": list(context["verification_scope"]),
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }

"""Validate the non-authoritative boundary of a blind external review result."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

REQUIRED_FIELDS = (
    "reviewer_id",
    "objective",
    "observations",
    "evidence_ids",
    "resolved_questions",
    "unresolved_questions",
    "falsifiable_points",
    "proposals",
    "interpretation",
    "human_gate",
)


def validate_blind_review_result(result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict):
        raise ValueError("result must be a mapping")

    missing = [field for field in REQUIRED_FIELDS if field not in result]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    if not str(result["reviewer_id"]).strip():
        raise ValueError("reviewer_id is required")
    if not str(result["objective"]).strip():
        raise ValueError("objective is required")

    for field in REQUIRED_FIELDS[2:-1]:
        if not isinstance(result[field], list):
            raise ValueError(f"{field} must be a list")

    human_gate = result["human_gate"]
    if not isinstance(human_gate, dict):
        raise ValueError("human_gate must be a mapping")
    if human_gate.get("required") is not True:
        raise ValueError("human_gate.required must remain true")
    if human_gate.get("decision") != "pending":
        raise ValueError("human_gate.decision must remain pending")

    return result


def load_and_validate(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        document = yaml.safe_load(handle)
    if not isinstance(document, dict) or "matome" not in document:
        raise ValueError("blind review document must contain a matome mapping")
    matome = document["matome"]
    validate_blind_review_result(matome)
    return matome

"""Structural validation for the new Protocol Candidate representation.

This validator inspects only the explicit StructuralValidationRepresentation
contract. It does not adapt to the legacy Mapping/YAML validator and does not
create authority, approval, or execution readiness.
"""

from __future__ import annotations

from typing import Any

try:
    from .protocol_candidate_validation import StructuralValidationRepresentation
except ImportError:
    from protocol_candidate_validation import StructuralValidationRepresentation


REQUIRED_CANDIDATE_FIELDS = {
    "candidate_identity",
    "origin_observation_identity",
    "origin",
    "intent",
    "assumptions",
    "inputs",
    "steps",
    "outputs",
    "constraints",
    "stop_conditions",
    "evidence_plan",
    "approval",
    "verification",
    "status",
    "authority",
    "executable",
}


def validate_structural_validation_representation(
    representation: StructuralValidationRepresentation,
) -> dict[str, Any]:
    """Return a non-authoritative structural validation result.

    The function validates only information explicitly present in the new
    representation. It never fabricates legacy fields or semantic judgments.
    """

    if not isinstance(representation, StructuralValidationRepresentation):
        return {
            "valid": False,
            "errors": ("representation must be a StructuralValidationRepresentation",),
            "candidate_identity": None,
            "origin_observation_identity": None,
            "authority": False,
            "executable": False,
        }

    errors: list[str] = []
    candidate = representation.candidate

    missing = sorted(REQUIRED_CANDIDATE_FIELDS - set(candidate))
    if missing:
        errors.append(
            "missing required candidate fields: " + ", ".join(missing)
        )

    if candidate.get("candidate_identity") != representation.candidate_identity:
        errors.append("candidate_identity does not match representation identity")

    if (
        candidate.get("origin_observation_identity")
        != representation.origin_observation_identity
    ):
        errors.append(
            "origin_observation_identity does not match representation identity"
        )

    if candidate.get("status") != "CANDIDATE":
        errors.append("candidate.status must be CANDIDATE")

    if candidate.get("authority") is not False or representation.authority is not False:
        errors.append("authority must remain false")

    if candidate.get("executable") is not False or representation.executable is not False:
        errors.append("executable must remain false")

    approval = candidate.get("approval")
    if not isinstance(approval, dict) and not hasattr(approval, "get"):
        errors.append("approval must be a mapping")
    else:
        if approval.get("required") is not True:
            errors.append("approval.required must be true")
        if approval.get("gate") != "HUMAN_REVIEW":
            errors.append("approval.gate must be HUMAN_REVIEW")

    verification = candidate.get("verification")
    if not isinstance(verification, dict) and not hasattr(verification, "get"):
        errors.append("verification must be a mapping")
    else:
        if verification.get("separate_from_execution") is not True:
            errors.append(
                "verification.separate_from_execution must be true"
            )

    origin = candidate.get("origin")
    if not isinstance(origin, dict) and not hasattr(origin, "get"):
        errors.append("origin must be a mapping")
    else:
        if origin.get("observation_identity") != representation.origin_observation_identity:
            errors.append("origin.observation_identity must preserve provenance")
        if not origin.get("provenance"):
            errors.append("origin.provenance must preserve provenance")
        if not origin.get("uncertainty"):
            errors.append("origin.uncertainty must be preserved")

    return {
        "valid": not errors,
        "errors": tuple(errors),
        "candidate_identity": representation.candidate_identity,
        "origin_observation_identity": representation.origin_observation_identity,
        "authority": False,
        "executable": False,
    }

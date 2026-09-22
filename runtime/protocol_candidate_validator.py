"""Structural validation for generated Protocol Candidates.

This validator checks only the generation/execution boundary contract.
It does not approve, promote, execute, or interpret Protocol semantics.
"""

from __future__ import annotations

from typing import Any, Mapping


REQUIRED_TOP_LEVEL = {
    "matome",
    "provenance",
    "intent",
    "boundary",
    "context",
    "behavior",
    "dead_mans_test",
    "quality_checks",
    "execution",
    "human_gate",
    "evidence",
    "fail_closed",
}

REQUIRED_PROVENANCE = {
    "candidate_identity",
    "generator_identity",
    "generation_context",
    "generation_timestamp",
    "source_evidence",
    "immutable",
}


def validate_protocol_candidate(
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a stable structural inspection result.

    Validation is deliberately non-authoritative: a valid candidate remains
    non-executable until the separate Human Gate promotes it.
    """

    errors: list[str] = []

    if not isinstance(candidate, Mapping):
        return {"valid": False, "errors": ("candidate must be a mapping",)}

    missing = sorted(REQUIRED_TOP_LEVEL - set(candidate))
    if missing:
        errors.append(f"missing required sections: {', '.join(missing)}")

    matome = candidate.get("matome")
    if not isinstance(matome, Mapping):
        errors.append("matome must be a mapping")
    else:
        if matome.get("status") != "candidate":
            errors.append("matome.status must be candidate")
        if matome.get("authority") is not False:
            errors.append("matome.authority must be false")
        if matome.get("executable") is not False:
            errors.append("matome.executable must be false")

    provenance = candidate.get("provenance")
    if not isinstance(provenance, Mapping):
        errors.append("provenance must be a mapping")
    else:
        missing_provenance = sorted(REQUIRED_PROVENANCE - set(provenance))
        if missing_provenance:
            errors.append(
                "missing provenance fields: "
                + ", ".join(missing_provenance)
            )
        if provenance.get("immutable") is not True:
            errors.append("provenance.immutable must be true")

    execution = candidate.get("execution")
    if not isinstance(execution, Mapping):
        errors.append("execution must be a mapping")
    else:
        forbidden_execution = {
            "approved": True,
            "approval_envelope": None,
            "activation": None,
            "scheduler": None,
            "runner": None,
        }
        for field, expected in forbidden_execution.items():
            if field not in execution:
                errors.append(f"execution.{field} is required")
            elif execution[field] != expected:
                errors.append(
                    f"execution.{field} violates candidate boundary"
                )

    human_gate = candidate.get("human_gate")
    if not isinstance(human_gate, Mapping):
        errors.append("human_gate must be a mapping")
    elif human_gate.get("required") is not True:
        errors.append("human_gate.required must be true")

    dead_mans_test = candidate.get("dead_mans_test")
    if not isinstance(dead_mans_test, Mapping):
        errors.append("dead_mans_test must be a mapping")
    elif dead_mans_test.get("result") != "pass":
        errors.append("dead_mans_test.result must be pass")

    quality_checks = candidate.get("quality_checks")
    if not isinstance(quality_checks, Mapping):
        errors.append("quality_checks must be a mapping")
    else:
        required_checks = {
            "observable_behavior",
            "required_behavior",
            "missing_information_check",
            "question_behavior",
            "boundary_check",
            "authority_check",
        }
        missing_checks = sorted(required_checks - set(quality_checks))
        if missing_checks:
            errors.append(
                "missing quality checks: " + ", ".join(missing_checks)
            )
        for name in required_checks & set(quality_checks):
            if quality_checks[name] != "pass":
                errors.append(f"quality_checks.{name} must be pass")

    return {
        "valid": not errors,
        "errors": tuple(errors),
        "candidate_identity": (
            provenance.get("candidate_identity")
            if isinstance(provenance, Mapping)
            else None
        ),
        "authority": False,
        "executable": False,
    }

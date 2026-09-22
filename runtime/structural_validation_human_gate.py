"""Explicit Structural Validation Result -> Human Gate input boundary."""

from __future__ import annotations

from typing import Any, Mapping

try:
    from .human_gate import HumanGateDecision, process_human_gate
except ImportError:
    from human_gate import HumanGateDecision, process_human_gate


def to_human_gate_input(
    validation_result: Mapping[str, Any],
) -> dict[str, Any]:
    """Map only validation identity/result into the existing Human Gate contract.

    No reviewer identity or human decision is inferred, and no approval is
    created by this adapter.
    """
    if not isinstance(validation_result, Mapping):
        raise TypeError("validation_result must be a mapping")

    candidate_identity = validation_result.get("candidate_identity")
    observation_identity = validation_result.get("origin_observation_identity")
    valid = validation_result.get("valid")

    if not candidate_identity:
        raise ValueError("missing candidate identity")
    if not observation_identity:
        raise ValueError("missing origin observation identity")
    if valid is not True:
        raise ValueError("validation result must be PASS")
    if validation_result.get("authority") is not False:
        raise ValueError("validation result must have no authority")
    if validation_result.get("executable") is not False:
        raise ValueError("validation result must not be executable")

    return {
        "candidate_identity": candidate_identity,
        "protocol_identity": candidate_identity,
        "provenance": (observation_identity,),
        "evidence_ids": (),
        "validation": True,
        "authority": False,
        "executable": False,
    }


def process_validated_candidate(
    *,
    validation_result: Mapping[str, Any],
    reviewer_identity: str,
    decision: str,
) -> HumanGateDecision:
    """Pass an explicit validated candidate to the existing Human Gate."""
    candidate = to_human_gate_input(validation_result)
    return process_human_gate(
        candidate=candidate,
        reviewer_identity=reviewer_identity,
        decision=decision,
    )

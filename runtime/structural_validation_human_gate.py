"""Explicit Structural Validation Result -> Human Gate input boundary."""

from __future__ import annotations

from typing import Any, Mapping

try:
    from .human_gate import HumanGateDecision, process_human_gate
except ImportError:
    from human_gate import HumanGateDecision, process_human_gate


REQUIRED_APPROVAL_METADATA = (
    "protocol_identity",
    "provenance",
    "evidence_ids",
)


def to_human_gate_input(
    validation_result: Mapping[str, Any],
) -> dict[str, Any]:
    """Map explicit approval metadata into the Human Gate contract.

    No protocol identity, provenance, or evidence linkage is inferred.
    """
    if not isinstance(validation_result, Mapping):
        raise TypeError("validation_result must be a mapping")

    candidate_identity = validation_result.get("candidate_identity")
    valid = validation_result.get("valid")

    if not candidate_identity:
        raise ValueError("missing candidate identity")
    if valid is not True:
        raise ValueError("validation result must be PASS")
    if validation_result.get("authority") is not False:
        raise ValueError("validation result must have no authority")
    if validation_result.get("executable") is not False:
        raise ValueError("validation result must not be executable")

    missing = [
        key for key in REQUIRED_APPROVAL_METADATA
        if key not in validation_result
    ]
    if missing:
        raise ValueError(
            "missing explicit approval metadata: " + ", ".join(missing)
        )

    protocol_identity = validation_result["protocol_identity"]
    provenance = validation_result["provenance"]
    evidence_ids = validation_result["evidence_ids"]

    if not protocol_identity:
        raise ValueError("protocol_identity is required")
    if not isinstance(provenance, (tuple, list)):
        raise ValueError("provenance must be an explicit sequence")
    if not isinstance(evidence_ids, (tuple, list)):
        raise ValueError("evidence_ids must be an explicit sequence")

    return {
        "candidate_identity": candidate_identity,
        "protocol_identity": protocol_identity,
        "provenance": tuple(provenance),
        "evidence_ids": tuple(evidence_ids),
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
    """Pass an explicitly enriched validated candidate to Human Gate."""
    candidate = to_human_gate_input(validation_result)
    return process_human_gate(
        candidate=candidate,
        reviewer_identity=reviewer_identity,
        decision=decision,
    )

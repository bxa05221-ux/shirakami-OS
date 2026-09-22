"""Explicit ApprovalEnvelope -> Activation input boundary.

This adapter is a representation handoff only. It preserves explicit
approval metadata and never creates, expands, or reinterprets authority.
"""

from __future__ import annotations

from typing import Any

try:
    from .approval_envelope import ApprovalEnvelope
except ImportError:
    from approval_envelope import ApprovalEnvelope


def to_activation_input(approval: ApprovalEnvelope) -> dict[str, Any]:
    """Map an immutable ApprovalEnvelope into the existing Activation contract."""
    if not isinstance(approval, ApprovalEnvelope):
        raise TypeError("approval must be an ApprovalEnvelope")

    if not approval.candidate_id:
        raise ValueError("candidate identity is required")
    if not approval.protocol_id:
        raise ValueError("protocol identity is required")
    if not approval.reviewer:
        raise ValueError("approval reviewer is required")
    if approval.execution_authorized is not True:
        raise ValueError("execution authorization is required")
    if approval.approval_scope not in {"execution", "publication"}:
        raise ValueError("approval scope is required")

    return {
        "candidate_id": approval.candidate_id,
        "protocol_id": approval.protocol_id,
        "reviewer": approval.reviewer,
        "provenance": tuple(approval.provenance),
        "evidence_ids": tuple(approval.evidence_ids),
        "execution_authorized": approval.execution_authorized,
        "approval_scope": approval.approval_scope,
    }

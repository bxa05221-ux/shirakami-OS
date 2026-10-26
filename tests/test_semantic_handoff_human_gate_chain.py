from runtime.approval_envelope import ApprovalEnvelope
from runtime.structural_validation_human_gate import (
    process_validated_candidate,
    to_human_gate_input,
)


def semantic_handoff_validation():
    """Minimal explicit SemanticHandoff-shaped approval metadata."""
    return {
        "candidate_identity": "candidate-semantic-001",
        "valid": True,
        "authority": False,
        "executable": False,
        "protocol_identity": "protocol-semantic-001",
        "provenance": ("observation-semantic-001",),
        "evidence_ids": ("evidence-shared-001", "evidence-local-001"),
    }


def test_semantic_handoff_evidence_identity_reaches_approval_envelope():
    handoff = semantic_handoff_validation()

    gate_input = to_human_gate_input(handoff)
    assert gate_input["protocol_identity"] == "protocol-semantic-001"
    assert gate_input["evidence_ids"] == (
        "evidence-shared-001",
        "evidence-local-001",
    )

    decision = process_validated_candidate(
        validation_result=handoff,
        reviewer_identity="human-semantic-001",
        decision="approve",
    )

    envelope = decision.approval_envelope
    assert isinstance(envelope, ApprovalEnvelope)
    assert envelope.protocol_id == "protocol-semantic-001"
    assert envelope.evidence_ids == (
        "evidence-shared-001",
        "evidence-local-001",
    )
    assert envelope.execution_authorized is True

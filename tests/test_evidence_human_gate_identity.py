from runtime.human_gate import process_human_gate


def test_evidence_ids_are_preserved_across_human_gate():
    evidence_ids = (
        "evidence-shared-001",
        "evidence-local-001",
        "evidence-shared-001",
    )
    candidate = {
        "candidate_identity": "candidate-test-identity-chain",
        "validation": True,
        "authority": False,
        "executable": False,
        "protocol_identity": "protocol-test-identity-chain",
        "provenance": ("generator-test", "source-test"),
        "evidence_ids": evidence_ids,
    }

    result = process_human_gate(
        candidate=candidate,
        reviewer_identity="human-test",
        decision="approve",
    )

    envelope = result.approval_envelope
    assert envelope is not None
    assert envelope.evidence_ids == evidence_ids
    assert envelope.execution_authorized is True

"""Authority non-propagation regression suite.

This suite protects the Human Gate boundary across Evidence, handoff metadata,
API approval input, and ApprovalEnvelope activation. Identifiers and transport
metadata may describe a decision, but they must not become authority by
inference.
"""

import pytest

from api.runtime_api import ShirakamiAPI
from runtime.approval_envelope import ApprovalEnvelope
from runtime.approval_envelope_activation import to_activation_input
from runtime.approval_envelope_provenance import enrich_human_gate_input


def test_evidence_id_does_not_authorize_execution():
    candidate = {
        "valid": True,
        "candidate_identity": "candidate-001",
        "protocol_identity": "protocol-001",
        "provenance": ("observation-001",),
        "evidence_ids": ("evidence-001",),
        "authority": False,
        "executable": False,
    }

    mapped = enrich_human_gate_input(candidate)

    assert mapped["evidence_ids"] == ("evidence-001",)
    assert mapped["authority"] is False
    assert mapped["executable"] is False


def test_semantic_handoff_metadata_does_not_authorize_execution():
    envelope = ApprovalEnvelope(
        candidate_id="candidate-001",
        protocol_id="protocol-001",
        provenance=("observation-001",),
        evidence_ids=("evidence-001",),
    )

    with pytest.raises(ValueError):
        to_activation_input(envelope)


def test_api_approval_requires_explicit_human_authorization():
    api = ShirakamiAPI()

    result = api.approve(
        approved=True,
        reviewer="human",
        human_authorized=False,
    )

    assert result["accepted"] is False
    assert "explicit human authorization required" in result["reason"]


def test_authorized_execution_is_created_only_by_explicit_envelope_action():
    envelope = ApprovalEnvelope(
        candidate_id="candidate-001",
        protocol_id="protocol-001",
        provenance=("observation-001",),
        evidence_ids=("evidence-001",),
    )

    authorized = envelope.authorize_execution("reviewer-001")
    activation = to_activation_input(authorized)

    assert activation["execution_authorized"] is True
    assert activation["reviewer"] == "reviewer-001"
    assert activation["approval_scope"] == "execution"

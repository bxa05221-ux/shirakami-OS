"""Tests for verified Agent Activity Evidence promotion."""

import pytest

from runtime.agent_activity import ingest_agent_activity
from runtime.agent_activity_evidence import AgentActivityEvidencePromoter
from runtime.agent_activity_verification import AgentActivityVerifier


def _verified_activity():
    activity = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
        result="read",
    )
    verification = AgentActivityVerifier().verify(
        activity,
        method="repository_state_check",
        verified=True,
        observed={"target_exists": True},
    )
    return activity, verification


def test_unverified_activity_cannot_be_promoted() -> None:
    activity = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
    )
    verification = AgentActivityVerifier().verify(
        activity,
        method="repository_state_check",
        verified=False,
    )

    with pytest.raises(ValueError, match="only verified"):
        AgentActivityEvidencePromoter().promote(
            activity,
            verification,
            human_gate_confirmed=True,
        )


def test_verified_activity_requires_explicit_human_gate() -> None:
    activity, verification = _verified_activity()

    with pytest.raises(ValueError, match="Human Gate"):
        AgentActivityEvidencePromoter().promote(activity, verification)


def test_verified_activity_promotes_to_evidence_with_provenance() -> None:
    activity, verification = _verified_activity()

    record, promotion = AgentActivityEvidencePromoter().promote(
        activity,
        verification,
        human_gate_confirmed=True,
    )

    assert record.evidence_id == promotion.evidence_id
    assert record.transition_kind == "external_agent_activity"
    assert record.transition_data["activity_id"] == activity.activity_id
    assert record.transition_data["verification"]["method"] == "repository_state_check"
    assert record.confidence == "verified"
    assert record.transition_data["execution_authorized"] is False
    assert record.transition_data["publish_authorized"] is False
    assert record.transition_data["merge_authorized"] is False
    assert record.transition_data["human_gate_required"] is True

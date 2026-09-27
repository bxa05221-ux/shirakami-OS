"""Boundary tests for external Agent Activity ingestion."""

from runtime.agent_activity import (
    AgentActivity,
    ActivityObservation,
    ingest_agent_activity,
)


def test_agent_activity_is_deterministically_identified() -> None:
    first = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
        timestamp="2026-09-26T00:00:00Z",
    )
    second = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
        timestamp="2026-09-26T00:00:00Z",
    )

    assert first.activity_id == second.activity_id


def test_activity_starts_as_unverified_and_non_authoritative() -> None:
    activity = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="search",
        target="ExecutionTrace",
    )

    assert activity.verification_status == "unverified"
    assert activity.self_reported is True
    assert not hasattr(activity, "execution_authorized")
    assert not hasattr(activity, "publish_authorized")
    assert not hasattr(activity, "merge_authorized")


def test_activity_becomes_observation_without_becoming_evidence() -> None:
    activity = ingest_agent_activity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="git_status",
        target="bxa05221-ux/shirakami-OS",
    )

    observation = ActivityObservation.from_activity(
        activity,
        handoff_id="handoff-review-001",
    )

    assert observation.activity_id == activity.activity_id
    assert observation.operation_type == "git_status"
    assert observation.verification_status == "unverified"
    assert observation.handoff_id == "handoff-review-001"
    assert not hasattr(observation, "evidence_id")


def test_activity_result_does_not_change_activity_identity_without_a_result_change() -> None:
    first = AgentActivity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
        input=None,
        result="content",
        timestamp="2026-09-26T00:00:00Z",
    )
    second = AgentActivity(
        agent_id="copilot",
        session_id="session-1",
        source="github-copilot-cli",
        operation_type="file_read",
        target="runtime/trace.py",
        input=None,
        result="different-content",
        timestamp="2026-09-26T00:00:00Z",
    )

    assert first.activity_id != second.activity_id

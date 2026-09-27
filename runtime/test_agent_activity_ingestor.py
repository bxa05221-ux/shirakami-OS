"""Tests for provider-neutral Agent Activity ingestion."""

from __future__ import annotations

import json

import pytest

from .agent_activity_ingestor import AgentActivityIngestor


def test_ingest_record_remains_unverified_and_authority_free():
    activity = AgentActivityIngestor().ingest_record(
        {
            "agent_id": "github-copilot-cli",
            "session_id": "session-1",
            "source": "github-copilot-cli-hook",
            "operation_type": "tool_call",
            "target": "C:/repo",
            "input": {"tool_name": "bash"},
            "result": {"result": {"type": "object"}},
            "timestamp": "2026-09-27T00:00:00Z",
            "provenance": {"hook_event": "postToolUse"},
            "self_reported": False,
        }
    )

    assert activity.agent_id == "github-copilot-cli"
    assert activity.source == "github-copilot-cli-hook"
    assert activity.verification_status == "unverified"
    assert activity.self_reported is False
    assert activity.activity_id


def test_ingest_file_reads_multiple_records(tmp_path):
    path = tmp_path / "agent-activity.jsonl"
    records = [
        {
            "source": "github-copilot-cli-hook",
            "operation_type": "session_start",
        },
        {
            "source": "github-copilot-cli-hook",
            "operation_type": "tool_call",
            "input": {"tool_name": "view"},
        },
    ]
    path.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )

    activities = AgentActivityIngestor().ingest_file(path)

    assert [item.operation_type for item in activities] == [
        "session_start",
        "tool_call",
    ]
    assert all(item.verification_status == "unverified" for item in activities)


def test_invalid_record_is_rejected():
    with pytest.raises(ValueError, match="missing required activity fields"):
        AgentActivityIngestor().ingest_record({"source": "hook"})


def test_invalid_json_is_rejected():
    with pytest.raises(ValueError, match="invalid JSON on line 1"):
        AgentActivityIngestor().ingest_lines(["not-json"])


def test_ingestion_does_not_promote_to_evidence():
    activity = AgentActivityIngestor().ingest_record(
        {
            "source": "github-copilot-cli-hook",
            "operation_type": "tool_call",
        }
    )

    assert not hasattr(activity, "evidence_id")
    assert not hasattr(activity, "execution_authorized")
    assert not hasattr(activity, "publish_authorized")
    assert not hasattr(activity, "merge_authorized")
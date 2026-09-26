"""Tests for the provider-neutral Copilot hook collector."""

from __future__ import annotations

import json

from experiments.copilot_activity_hook import capture, normalize_hook_event


def test_pre_tool_use_becomes_unverified_tool_activity() -> None:
    activity = normalize_hook_event({
        "sessionId": "session-1",
        "timestamp": 1769472000000,
        "cwd": "C:/repo",
        "toolName": "bash",
        "toolArgs": {"command": "git status"},
    })
    assert activity["source"] == "github-copilot-cli-hook"
    assert activity["operation_type"] == "tool_call"
    assert activity["self_reported"] is False
    assert activity["verification_status"] == "unverified"
    assert activity["input"]["tool_name"] == "bash"


def test_post_tool_use_captures_result_without_authority() -> None:
    activity = normalize_hook_event({
        "hook_event_name": "postToolUse",
        "sessionId": "session-1",
        "timestamp": 1769472000000,
        "cwd": "C:/repo",
        "toolName": "view",
        "toolArgs": {"path": "runtime/trace.py"},
        "toolResult": {"resultType": "success", "textResultForLlm": "content"},
    })
    assert activity["operation_type"] == "tool_call"
    assert activity["result"]["resultType"] == "success"
    assert activity["verification_status"] == "unverified"
    assert "execution_authorized" not in activity
    assert "publish_authorized" not in activity
    assert "merge_authorized" not in activity


def test_capture_writes_jsonl_and_redacts_credentials(tmp_path) -> None:
    path = tmp_path / "activity.jsonl"
    capture({
        "hook_event_name": "postToolUse",
        "sessionId": "session-1",
        "timestamp": 1769472000000,
        "cwd": "C:/repo",
        "toolName": "bash",
        "toolArgs": {
            "command": "curl",
            "Authorization": "Bearer super-secret",
            "api_key": "secret-value",
        },
    }, path)
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["input"]["tool_input"]["Authorization"] == "[REDACTED]"
    assert record["input"]["tool_input"]["api_key"] == "[REDACTED]"
    assert record["verification_status"] == "unverified"


def test_session_events_are_captured() -> None:
    activity = normalize_hook_event({
        "hook_event_name": "SessionStart",
        "session_id": "session-1",
        "timestamp": "2026-09-26T00:00:00Z",
        "cwd": "/repo",
        "source": "startup",
    })
    assert activity["operation_type"] == "session_start"
    assert activity["session_id"] == "session-1"

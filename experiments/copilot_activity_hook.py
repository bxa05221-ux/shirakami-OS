"""Capture Copilot CLI hook events as unverified Shirakami Agent Activity."""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SECRET_KEY = re.compile(r"(token|secret|password|api[_-]?key|authorization|credential)", re.IGNORECASE)
_LOG_PATH = Path(".github/hooks/logs/agent-activity.jsonl")


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if _SECRET_KEY.search(str(key)) else _redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, str):
        return re.sub(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+", r"\1[REDACTED]", value)
    return value


def normalize_hook_event(payload: dict[str, Any]) -> dict[str, Any]:
    event = payload.get("hook_event_name") or payload.get("event") or "unknown"
    session_id = payload.get("session_id") or payload.get("sessionId")
    timestamp = payload.get("timestamp")
    if isinstance(timestamp, (int, float)):
        timestamp = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).isoformat()

    tool_name = payload.get("tool_name") or payload.get("toolName")
    tool_input = payload.get("tool_input", payload.get("toolArgs"))
    tool_result = payload.get("tool_result", payload.get("toolResult"))
    target = payload.get("cwd")

    if event in {"preToolUse", "PreToolUse", "postToolUse", "PostToolUse"}:
        operation_type, result = "tool_call", tool_result
    elif event in {"postToolUseFailure", "PostToolUseFailure"}:
        operation_type, result = "tool_call", {"error": payload.get("error")}
    elif event in {"userPromptSubmitted", "UserPromptSubmit"}:
        operation_type, result = "prompt_submission", None
        tool_input = payload.get("prompt")
    elif event in {"sessionStart", "SessionStart"}:
        operation_type, result = "session_start", None
    elif event in {"sessionEnd", "SessionEnd"}:
        operation_type, result = "session_end", {"reason": payload.get("reason")}
    elif event in {"agentStop", "Stop"}:
        operation_type, result = "agent_stop", {"stop_reason": payload.get("stop_reason") or payload.get("stopReason")}
    elif event == "subagentStart":
        operation_type, result = "subagent_start", None
    elif event in {"subagentStop", "SubagentStop"}:
        operation_type, result = "subagent_stop", {"stop_reason": payload.get("stop_reason") or payload.get("stopReason")}
    else:
        operation_type, result = "copilot_hook_event", None

    activity_input = tool_input if tool_name is None else {"tool_name": tool_name, "tool_input": tool_input}

    return {
        "agent_id": "github-copilot-cli",
        "session_id": session_id,
        "source": "github-copilot-cli-hook",
        "operation_type": operation_type,
        "target": target,
        "input": activity_input,
        "result": result,
        "timestamp": timestamp,
        "provenance": {
            "hook_event": event,
            "cwd": payload.get("cwd"),
            "host_pid": os.getpid(),
        },
        "self_reported": False,
        "verification_status": "unverified",
    }


def capture(payload: dict[str, Any], log_path: Path = _LOG_PATH) -> dict[str, Any]:
    activity = normalize_hook_event(_redact(payload))
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(activity, ensure_ascii=False, sort_keys=True))
        handle.write("\n")
    return activity


def main() -> None:
    raw = sys.stdin.read().strip()
    if raw:
        capture(json.loads(raw))


if __name__ == "__main__":
    main()

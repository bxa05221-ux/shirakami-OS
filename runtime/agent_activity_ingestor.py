"""Ingest provider-neutral Agent Activity records from local JSONL.

Hook output is treated as an unverified observation. This module never
promotes records to Evidence and never grants authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .agent_activity import AgentActivity, ingest_agent_activity


class AgentActivityIngestor:
    """Convert local activity records into unverified AgentActivity objects."""

    def ingest_record(self, record: dict[str, Any]) -> AgentActivity:
        required = ("source", "operation_type")
        missing = [key for key in required if not record.get(key)]
        if missing:
            raise ValueError(f"missing required activity fields: {', '.join(missing)}")

        return ingest_agent_activity(
            agent_id=record.get("agent_id"),
            session_id=record.get("session_id"),
            source=str(record["source"]),
            operation_type=str(record["operation_type"]),
            target=record.get("target"),
            input=record.get("input"),
            result=record.get("result"),
            timestamp=record.get("timestamp"),
            provenance=record.get("provenance") or {},
            self_reported=bool(record.get("self_reported", True)),
        )

    def ingest_lines(self, lines: Iterable[str]) -> list[AgentActivity]:
        activities: list[AgentActivity] = []
        for line_number, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"activity record on line {line_number} is not an object")
            activities.append(self.ingest_record(record))
        return activities

    def ingest_file(self, path: str | Path) -> list[AgentActivity]:
        with Path(path).open("r", encoding="utf-8") as handle:
            return self.ingest_lines(handle)
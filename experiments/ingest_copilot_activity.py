"""Ingest locally captured Copilot CLI activity without promoting it.

Usage:
    python experiments/ingest_copilot_activity.py
    python experiments/ingest_copilot_activity.py path/to/agent-activity.jsonl
"""

from __future__ import annotations

import sys
from pathlib import Path

from runtime.agent_activity_ingestor import AgentActivityIngestor

DEFAULT_PATH = Path(".github/hooks/logs/agent-activity.jsonl")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    if not path.exists():
        print(f"activity log not found: {path}")
        return 2

    activities = AgentActivityIngestor().ingest_file(path)
    print(f"ingested: {len(activities)}")
    for activity in activities:
        print(
            f"{activity.activity_id[:12]} "
            f"{activity.operation_type} "
            f"verification={activity.verification_status} "
            f"authority=none"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

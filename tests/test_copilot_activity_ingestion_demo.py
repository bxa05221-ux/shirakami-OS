from __future__ import annotations

import json
from pathlib import Path

from experiments.ingest_copilot_activity import main


def test_copilot_activity_ingestion_demo_reads_jsonl(tmp_path: Path, monkeypatch, capsys):
    log_path = tmp_path / "agent-activity.jsonl"
    log_path.write_text(
        json.dumps(
            {
                "agent_id": "github-copilot-cli",
                "source": "github-copilot-cli-hook",
                "operation_type": "tool_call",
                "verification_status": "unverified",
                "self_reported": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        ["ingest_copilot_activity.py", str(log_path)],
    )

    assert main() == 0

    output = capsys.readouterr().out
    assert "ingested: 1" in output
    assert "tool_call" in output
    assert "verification=unverified" in output
    assert "authority=none" in output

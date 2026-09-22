from pathlib import Path

from runtime.local_repository_runtime_evidence import execute_local_repository_protocol

MATOME = """
matome:
  protocol_id: local.observation
  title: Local observation
  version: "0.1"
  statement: >
    Observe a local repository protocol through the existing Runtime boundary.
  pipeline:
    - phase: observe
      action: inspect
"""


def test_local_repository_protocol_reaches_runtime_evidence_and_landscape(tmp_path: Path):
    protocol_path = tmp_path / "protocol.yaml"
    protocol_path.write_text(MATOME, encoding="utf-8")
    result = execute_local_repository_protocol(
        tmp_path,
        "protocol.yaml",
        landscape={"state": "ready", "owner": "human"},
        input_data={"message": "observed locally"},
    )
    assert result.protocol.protocol_id == "local.observation"
    assert result.protocol.version == "0.1"
    assert result.execution.status == "completed"
    assert result.evidence.protocol_id == "local.observation"
    assert result.evidence.transition_data["input"]["message"] == "observed locally"
    assert result.evidence.transition_data["changed"] is True
    assert result.landscape["state"] == "ready"
    assert result.landscape["owner"] == "human"
    assert result.landscape["protocol_id"] == "local.observation"


def test_local_repository_execution_does_not_create_judgment_fields(tmp_path: Path):
    (tmp_path / "protocol.yaml").write_text(MATOME, encoding="utf-8")
    result = execute_local_repository_protocol(
        tmp_path,
        "protocol.yaml",
        landscape={"state": "ready"},
        input_data={"human_gate": "pending"},
    )
    assert result.landscape["state"] == "ready"
    assert result.landscape["input"]["human_gate"] == "pending"
    assert "judgment" not in result.landscape
    assert "decision" not in result.landscape

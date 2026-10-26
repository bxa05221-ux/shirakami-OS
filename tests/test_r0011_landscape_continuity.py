from runtime.execute import execute_current_protocol
from runtime.protocol_registry import ProtocolRegistry


def test_r0011_execution_keeps_protocol_and_landscape_lineage_as_input_data(tmp_path):
    protocol_path = tmp_path / "protocol.yaml"
    protocol_path.write_text(
        """matome:
  title: R0011.continuity.v1
  version: 0.1
  statement: >
    Preserve lineage without asserting continuity.
  pipeline:
    - phase: observe
      action: record
""",
        encoding="utf-8",
    )

    registry = ProtocolRegistry()
    registry.register("r0011.continuity.v1", str(protocol_path))

    result = execute_current_protocol(
        str(protocol_path),
        registry,
        "r0011.continuity.v1",
        input_data={
            "landscape_state_id": "landscape-r0011-001",
            "transition_id": "transition-v1-001",
            "evidence_id": "evidence-v1-001",
        },
    )

    assert result["protocol_id"] == "r0011.continuity.v1"
    assert result["version"] == "0.1"
    assert result["input"]["landscape_state_id"] == "landscape-r0011-001"
    assert result["input"]["transition_id"] == "transition-v1-001"
    assert result["input"]["evidence_id"] == "evidence-v1-001"
    assert result["status"] == "prepared"


def test_r0011_current_execution_boundary_does_not_claim_continuity(tmp_path):
    protocol_path = tmp_path / "protocol.yaml"
    protocol_path.write_text(
        """matome:
  title: R0011.continuity.v2
  version: 0.2
  statement: >
    A new protocol must not imply continuity by itself.
  pipeline:
    - phase: transition
      action: prepare
""",
        encoding="utf-8",
    )

    registry = ProtocolRegistry()
    registry.register("r0011.continuity.v2", str(protocol_path))

    result = execute_current_protocol(
        str(protocol_path),
        registry,
        "r0011.continuity.v2",
        input_data={
            "input_landscape_state": "landscape-r001-001",
            "resulting_landscape_state": "landscape-r0011-002",
            "continuity_claim": "unverified",
        },
    )

    assert result["protocol_id"] == "r0011.continuity.v2"
    assert result["input"]["continuity_claim"] == "unverified"
    assert "continuity" not in result

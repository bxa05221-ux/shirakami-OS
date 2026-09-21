"""Selected Protocol A -> B composition through Runtime -> Evidence.

The compatibility assertion is intentionally structural; semantic compatibility
remains unknown unless a Protocol contract or explicit verification establishes it.
"""

from pathlib import Path

from runtime.execution_evidence import execute_current_protocol_with_evidence
from runtime.protocol_loader import load_matome
from runtime.protocol_registry import ProtocolRegistry


def _write_protocol(path: Path, title: str, input_name: str, output_name: str) -> None:
    path.write_text(
        f"""matome:
  title: {title}
  version: v0.1
  statement: >
    Selected composition fixture for boundary verification.
  pipeline:
    - phase: observe
      action: record
input:
  - {input_name}
output:
  - {output_name}
""",
        encoding="utf-8",
    )


def _registry_for(path: Path) -> ProtocolRegistry:
    protocol = load_matome(path)
    registry = ProtocolRegistry()
    registry.register_temporary(protocol.protocol_id, protocol)
    return registry


def test_selected_a_to_b_composition_reaches_evidence(tmp_path: Path) -> None:
    source = tmp_path / "protocol-a.yaml"
    target = tmp_path / "protocol-b.yaml"
    _write_protocol(source, "Protocol A", "context", "context")
    _write_protocol(target, "Protocol B", "context", "evidence")

    source_protocol = load_matome(source)
    source_result = execute_current_protocol_with_evidence(
        source,
        _registry_for(source),
        source_protocol.protocol_id,
        {"context": "A-output"},
    )

    source_output = source_result.evidence.transition_data["input"]
    assert source_output == {"context": "A-output"}

    target_protocol = load_matome(target)
    target_result = execute_current_protocol_with_evidence(
        target,
        _registry_for(target),
        target_protocol.protocol_id,
        source_output,
    )

    assert target_result.execution.status == "completed"
    assert target_result.evidence.status == "completed"
    assert target_result.evidence.transition_data["input"] == {"context": "A-output"}
    assert target_result.evidence.transition_data["changed"] is True

from pathlib import Path

from runtime.execute import execute_current_protocol
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry


PROTOCOL = """matome:
  title: MVP Test Protocol
  version: 0.1
  statement: >
    Minimal execution test
  pipeline:
    - phase: observe
      action: record
"""


def test_execute_current_protocol_returns_runtime_result(tmp_path: Path):
    path = tmp_path / "protocol.yaml"
    path.write_text(PROTOCOL, encoding="utf-8")

    protocol = parse_matome(PROTOCOL)
    registry = ProtocolRegistry()
    registry.register(protocol.protocol_id, protocol, state="active")

    result = execute_current_protocol(
        str(path), registry, protocol.protocol_id, {"message": "hello"}
    )

    assert result["protocol_id"] == protocol.protocol_id
    assert result["version"] == "0.1"
    assert result["input"] == {"message": "hello"}
    assert result["status"] == "prepared"

from pathlib import Path

import pytest

from runtime.current_protocol import CurrentProtocolError, load_current_protocol
from runtime.protocol_loader import parse_matome
from runtime.protocol_registry import ProtocolRegistry


PROTOCOL = """matome:
  title: Tsugaru Guide Highschool
  version: 0.1
  statement: >
    Test protocol
  pipeline:
    - phase: observe
      action: record
"""


def test_current_loader_accepts_registered_active_protocol(tmp_path: Path):
    path = tmp_path / "protocol.yaml"
    path.write_text(PROTOCOL, encoding="utf-8")

    parsed = parse_matome(PROTOCOL)
    registry = ProtocolRegistry()
    registry.register(parsed.protocol_id, parsed, state="active")

    current = load_current_protocol(path, registry, parsed.protocol_id)
    assert current.protocol_id == parsed.protocol_id
    assert current.version == "0.1"


def test_current_loader_rejects_archived_protocol(tmp_path: Path):
    path = tmp_path / "protocol.yaml"
    path.write_text(PROTOCOL, encoding="utf-8")

    parsed = parse_matome(PROTOCOL)
    registry = ProtocolRegistry()
    registry.register(parsed.protocol_id, parsed, state="archived")

    with pytest.raises(CurrentProtocolError):
        load_current_protocol(path, registry, parsed.protocol_id)


def test_current_loader_rejects_registry_file_mismatch(tmp_path: Path):
    path = tmp_path / "protocol.yaml"
    path.write_text(PROTOCOL, encoding="utf-8")

    registry = ProtocolRegistry()
    registry.register("another.protocol", object(), state="active")

    with pytest.raises(CurrentProtocolError):
        load_current_protocol(path, registry, "another.protocol")

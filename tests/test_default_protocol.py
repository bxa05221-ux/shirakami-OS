import pytest

from runtime.default_protocol import DEFAULT_PROTOCOL_ID, bootstrap_default_protocol
from runtime.protocol_api import (
    build_default_protocol_request,
    register_temporary_matome,
)
from runtime.protocol_registry import ProtocolRegistry, ProtocolRegistryError


MATOME_YAML = """matome:
  title: session guide
  version: 0.1
  statement: >
    Use the stabilized interaction flow as a temporary reusable Protocol.
  pipeline:
    - phase: observation
      action: capture
    - phase: response
      action: render
"""


def test_bootstrap_registers_mandatory_default_protocol():
    registry = ProtocolRegistry()
    entry = bootstrap_default_protocol(registry)

    assert entry.protocol_id == DEFAULT_PROTOCOL_ID
    assert entry.lifecycle == "default"
    assert entry.state == "active"
    assert registry.require_default() == entry


def test_bootstrap_is_idempotent():
    registry = ProtocolRegistry()
    first = bootstrap_default_protocol(registry)
    second = bootstrap_default_protocol(registry)

    assert second == first
    assert len(registry.snapshot()) == 1


def test_default_protocol_request_uses_same_request_boundary():
    registry = ProtocolRegistry()
    bootstrap_default_protocol(registry)

    request = build_default_protocol_request(registry, {"message": "hello"})

    assert request.protocol_id == DEFAULT_PROTOCOL_ID
    assert request.version == "0.1"
    assert request.input == {"message": "hello"}


def test_default_protocol_cannot_be_removed_or_archived():
    registry = ProtocolRegistry()
    entry = bootstrap_default_protocol(registry)

    with pytest.raises(ProtocolRegistryError):
        registry.remove(entry.protocol_id)
    with pytest.raises(ProtocolRegistryError):
        registry.set_state(entry.protocol_id, "archived")


def test_only_one_default_protocol_can_exist():
    registry = ProtocolRegistry()
    registry.register_default("default-a", {"version": "1.0"})

    with pytest.raises(ProtocolRegistryError):
        registry.register_default("default-b", {"version": "1.0"})


def test_temporary_matome_protocol_can_be_registered_replaced_and_removed():
    registry = ProtocolRegistry()
    bootstrap_default_protocol(registry)

    entry = register_temporary_matome(registry, MATOME_YAML)
    assert entry.lifecycle == "temporary"
    assert entry.protocol_id == "session.guide"
    assert entry.artifact.version == "0.1"

    replaced = registry.replace_temporary("session.guide", {"version": "0.2"})
    assert replaced.artifact["version"] == "0.2"

    registry.remove("session.guide")
    with pytest.raises(ProtocolRegistryError):
        registry.get("session.guide")
    assert registry.require_default().protocol_id == DEFAULT_PROTOCOL_ID


def test_temporary_protocol_cannot_replace_default():
    registry = ProtocolRegistry()
    bootstrap_default_protocol(registry)

    with pytest.raises(ProtocolRegistryError):
        registry.replace_temporary(DEFAULT_PROTOCOL_ID, {"version": "2.0"})

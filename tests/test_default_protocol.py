from runtime.default_protocol import DEFAULT_PROTOCOL_ID, bootstrap_default_protocol
from runtime.protocol_registry import ProtocolRegistry


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

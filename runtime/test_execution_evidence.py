"""Tests for the explicit Registry-selected execution/evidence boundary."""

from pathlib import Path

import pytest

from runtime.execution_evidence import execute_current_protocol_with_evidence
from runtime.protocol_loader import load_matome
from runtime.protocol_registry import ProtocolRegistry, ProtocolRegistryError


PROTOCOL = Path(__file__).resolve().parents[1] / "protocols" / "manual" / "manga-user-manual.yaml"


def _registry_for_protocol(protocol):
    registry = ProtocolRegistry()
    registry.register_temporary(protocol.protocol_id, protocol)
    return registry


def test_registry_selected_execution_captures_evidence():
    protocol = load_matome(PROTOCOL)
    registry = _registry_for_protocol(protocol)

    result = execute_current_protocol_with_evidence(
        PROTOCOL,
        registry,
        protocol.protocol_id,
        {"language": "ja"},
    )

    assert result.protocol == protocol
    assert result.execution.status == "completed"
    assert result.execution.protocol_id == protocol.protocol_id
    assert result.evidence.protocol_id == protocol.protocol_id
    assert result.evidence.status == "completed"
    assert result.evidence.transition_kind == "matome.protocol.transition"
    assert result.evidence.transition_data["input"] == {"language": "ja"}
    assert result.evidence.transition_data["changed"] is True


def test_archived_protocol_cannot_reach_execution_boundary():
    protocol = load_matome(PROTOCOL)
    registry = _registry_for_protocol(protocol)
    registry.set_state(protocol.protocol_id, "archived")

    with pytest.raises(ProtocolRegistryError):
        execute_current_protocol_with_evidence(
            PROTOCOL,
            registry,
            protocol.protocol_id,
        )

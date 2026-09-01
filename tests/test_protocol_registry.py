import pytest

from runtime.protocol_registry import ProtocolRegistry, ProtocolRegistryError


def test_archived_protocol_is_preserved_but_not_current():
    registry = ProtocolRegistry()
    registry.register("cheseborough-vr", {"title": "Cheseborough VR"}, state="archived")

    assert registry.get("cheseborough-vr").state == "archived"
    assert registry.get("cheseborough-vr").artifact["title"] == "Cheseborough VR"
    with pytest.raises(ProtocolRegistryError):
        registry.select_current("cheseborough-vr")


def test_active_protocol_is_current_candidate():
    registry = ProtocolRegistry()
    registry.register("tsugaru-guide-highschool", {"title": "TSUGARU GUIDE HIGH SCHOOL"}, state="active")

    current = registry.select_current("tsugaru-guide-highschool")
    assert current.protocol_id == "tsugaru-guide-highschool"
    assert current.state == "active"


def test_experimental_protocol_remains_selectable():
    registry = ProtocolRegistry()
    registry.register("draft", {"title": "Draft"}, state="experimental")

    assert registry.select_current("draft").state == "experimental"
    assert [entry.protocol_id for entry in registry.list_current_candidates()] == ["draft"]


def test_state_transition_does_not_delete_artifact():
    registry = ProtocolRegistry()
    artifact = {"historical_id": "cheseborough-vr"}
    registry.register("legacy", artifact, state="active")
    registry.set_state("legacy", "archived")

    assert registry.get("legacy").artifact == artifact
    assert registry.get("legacy").state == "archived"

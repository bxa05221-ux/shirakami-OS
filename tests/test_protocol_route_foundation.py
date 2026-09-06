import pytest

from runtime.protocol_api import (
    build_default_protocol_request,
    build_protocol_request,
    register_temporary_matome,
)
from runtime.protocol_registry import ProtocolRegistry, ProtocolRegistryError
from runtime.route_map import RouteMap, RouteMapError


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


def test_protocol_request_uses_registered_matome_as_parameter():
    registry = ProtocolRegistry()
    artifact = {"version": "1.2.1", "title": "Thread RPG"}
    registry.register("thread-rpg", artifact, state="active")

    request = build_protocol_request(
        registry,
        "thread-rpg",
        {"message": "hello"},
    )

    assert request.protocol_id == "thread-rpg"
    assert request.version == "1.2.1"
    assert request.input == {"message": "hello"}


def test_explicit_request_version_overrides_default_parameter():
    registry = ProtocolRegistry()
    registry.register("demo", {"version": "1.0"}, state="active")

    request = build_protocol_request(registry, "demo", version="2.0")

    assert request.version == "2.0"


def test_archived_protocol_cannot_be_invoked():
    registry = ProtocolRegistry()
    registry.register("old", {"version": "1.0"}, state="archived")

    with pytest.raises(ValueError):
        build_protocol_request(registry, "old")


def test_default_protocol_is_permanent_and_required():
    registry = ProtocolRegistry()
    registry.register_default("default", {"version": "1.0"})

    request = build_default_protocol_request(registry, {"message": "hello"})

    assert request.protocol_id == "default"
    assert registry.require_default().lifecycle == "default"

    with pytest.raises(ProtocolRegistryError):
        registry.remove("default")


def test_default_request_fails_when_default_is_missing():
    registry = ProtocolRegistry()

    with pytest.raises(ValueError):
        build_default_protocol_request(registry)


def test_default_protocol_cannot_be_archived():
    registry = ProtocolRegistry()
    registry.register_default("default", {"version": "1.0"})

    with pytest.raises(ProtocolRegistryError):
        registry.set_state("default", "archived")


def test_only_one_default_protocol_can_exist():
    registry = ProtocolRegistry()
    registry.register_default("default-a", {"version": "1.0"})

    with pytest.raises(ProtocolRegistryError):
        registry.register_default("default-b", {"version": "1.0"})


def test_temporary_matome_protocol_can_be_replaced_and_removed():
    registry = ProtocolRegistry()
    registry.register_default("default", {"version": "1.0"})
    registry.register_temporary("session-guide", {"version": "0.1"})

    replaced = registry.replace_temporary("session-guide", {"version": "0.2"})
    assert replaced.lifecycle == "temporary"
    assert replaced.artifact["version"] == "0.2"

    registry.remove("session-guide")
    with pytest.raises(ProtocolRegistryError):
        registry.get("session-guide")
    assert registry.require_default().protocol_id == "default"


def test_default_protocol_cannot_be_replaced_as_temporary():
    registry = ProtocolRegistry()
    registry.register_default("default", {"version": "1.0"})

    with pytest.raises(ProtocolRegistryError):
        registry.replace_temporary("default", {"version": "2.0"})


def test_stabilized_matome_yaml_becomes_temporary_protocol():
    registry = ProtocolRegistry()
    registry.register_default("default", {"version": "1.0"})

    entry = register_temporary_matome(registry, MATOME_YAML)

    assert entry.lifecycle == "temporary"
    assert entry.protocol_id == "session.guide"
    assert entry.artifact.version == "0.1"
    assert registry.get("session.guide").artifact.title == "session guide"


def test_invalid_matome_yaml_is_not_registered():
    registry = ProtocolRegistry()

    with pytest.raises(ValueError):
        register_temporary_matome(registry, "matome:\n  title: broken\n")

    assert registry.list_current_candidates() == []


def test_route_map_exposes_next_protocols_without_interpreting_them():
    route = RouteMap.from_mapping(
        "observation",
        {
            "observation": ["conversation", "reflection"],
            "conversation": ["observation"],
        },
    )

    assert route.current == "observation"
    assert route.next_protocols() == ("conversation", "reflection")
    assert route.can_transition("conversation") is True
    assert route.can_transition("unknown") is False


def test_route_move_requires_explicit_edge():
    route = RouteMap.from_mapping("a", {"a": ["b"], "b": []})

    moved = route.move("b")

    assert moved.current == "b"
    assert moved.snapshot()["current"] == "b"

    with pytest.raises(RouteMapError):
        moved.move("c")

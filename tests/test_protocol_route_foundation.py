import pytest

from runtime.protocol_api import build_protocol_request
from runtime.protocol_registry import ProtocolRegistry
from runtime.route_map import RouteMap, RouteMapError


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

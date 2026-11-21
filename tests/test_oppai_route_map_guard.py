"""Contract checks for the opt-in OPPAI RouteMap selection boundary."""

from unittest.mock import patch

import pytest

from runtime.oppai_runtime_flow import (
    build_selected_protocol_request,
    execute_selected_pipeline,
)
from runtime.route_map import RouteMap


def _map():
    return RouteMap.from_mapping(
        "thread_rpg",
        {"thread_rpg": ("perspective",)},
    )


def test_disallowed_route_is_rejected_before_registry_or_adapter():
    with pytest.raises(PermissionError, match="not permitted"):
        build_selected_protocol_request(
            "test", None, "radio", route_map=_map(), require_route_map=True
        )


def test_missing_route_map_fails_closed_when_required():
    with pytest.raises(PermissionError, match="RouteMap is required"):
        build_selected_protocol_request(
            "test", None, "perspective", require_route_map=True
        )


def test_explicitly_allowed_route_reaches_existing_request_builder():
    sentinel = object()
    with patch(
        "runtime.oppai_runtime_flow.build_protocol_request",
        return_value=sentinel,
    ) as builder:
        result = build_selected_protocol_request(
            "test", None, "perspective", route_map=_map(), require_route_map=True
        )
    assert result is sentinel
    builder.assert_called_once()
    assert builder.call_args.args[1] == "perspective"


def test_selected_pipeline_rejects_before_adapter_or_registry_execution():
    class NeverCallAdapter:
        def execute(self, request):
            raise AssertionError("adapter must not execute")

    with pytest.raises(PermissionError, match="not permitted"):
        execute_selected_pipeline(
            "test",
            None,
            "radio",
            NeverCallAdapter(),
            route_map=_map(),
            require_route_map=True,
        )


def test_route_recording_does_not_authorize_selection():
    route = _map().record_transition("radio")
    # A recorded edge is observable history, not independent authorization.
    # The original allowlist remains the authority for a constrained request.
    with pytest.raises(PermissionError, match="not permitted"):
        build_selected_protocol_request(
            "test", None, "radio", route_map=_map(), require_route_map=True
        )
    assert "radio" in route.transitions["thread_rpg"]
    assert route.current == "radio"
    assert not route.can_transition("radio")

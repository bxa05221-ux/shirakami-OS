"""Tests for the State -> Matrix -> Protocol routing MVP."""

from runtime.routing import derive_matrix_state, route_protocol


def test_matrix_state_is_derived_deterministically():
    context = {
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
        "evidence": ["E-001"],
    }
    assert derive_matrix_state(context).priority == 2
    assert derive_matrix_state(context).phase == 1
    assert derive_matrix_state(context).relation == 3


def test_protocol_is_selected_from_explicit_state_and_evidence():
    context = {
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
        "evidence": ["E-001"],
    }
    protocols = {
        "protocol.alpha": {
            "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
            "required_evidence": ["E-001"],
        },
        "protocol.beta": {
            "accepted_states": [{"priority": 1, "phase": 1, "relation": 3}],
            "required_evidence": ["E-001"],
        },
    }

    result = route_protocol(context, protocols)

    assert result.status == "ready"
    assert result.selected_protocol == "protocol.alpha"


def test_missing_evidence_blocks_routing():
    context = {
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
        "evidence": [],
    }
    protocols = {
        "protocol.alpha": {
            "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
            "required_evidence": ["E-001"],
        }
    }

    result = route_protocol(context, protocols)

    assert result.status == "blocked"
    assert result.selected_protocol is None


def test_routing_does_not_execute_protocol():
    called = False

    def fake_protocol():
        nonlocal called
        called = True

    context = {"matrix": {"priority": 2, "phase": 1, "relation": 3}}
    result = route_protocol(context, {"protocol.alpha": {}})

    assert result.status == "ready"
    assert called is False

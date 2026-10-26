"""Tests for deterministic Prompt assembly."""

import pytest

from runtime.prompt import assemble_prompt
from runtime.routing import route_protocol


def test_prompt_assembly_preserves_routing_context():
    context = {
        "version": "1.0",
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
        "evidence": ["E-001"],
        "uncertainty": ["U-001"],
    }
    routing = route_protocol(
        context,
        {
            "protocol.alpha": {
                "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
                "required_evidence": ["E-001"],
            }
        },
    )

    prompt = assemble_prompt(
        prompt_id="P-001",
        version="0.1",
        routing_result=routing,
        context=context,
    )

    assert prompt.protocol_id == "protocol.alpha"
    assert prompt.version == "0.1"
    assert prompt.context["matrix"]["priority"] == 2
    assert prompt.evidence == ("E-001",)
    assert prompt.uncertainty == ("U-001",)
    assert "Do not make a final human decision." in prompt.instructions


def test_blocked_routing_cannot_become_prompt():
    context = {"version": "1.0", "matrix": {"priority": 2, "phase": 1, "relation": 3}}
    routing = route_protocol(
        context,
        {
            "protocol.alpha": {
                "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
                "required_evidence": ["E-001"],
            }
        },
    )

    with pytest.raises(ValueError):
        assemble_prompt(
            prompt_id="P-002",
            version="0.1",
            routing_result=routing,
            context=context,
        )

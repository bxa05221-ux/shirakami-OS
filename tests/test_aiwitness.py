"""Tests for AIwitness simulation integration."""

from runtime.prompt import assemble_prompt
from runtime.routing import route_protocol
from runtime.simulation import execute_simulation
from runtime.aiwitness import record_simulation_witness


def test_witness_links_prompt_protocol_simulation_and_evidence():
    context = {
        "version": "1.0",
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
        "evidence": ["E-001", "E-002"],
        "uncertainty": ["U-001"],
    }
    routing = route_protocol(
        context,
        {"protocol.alpha": {
            "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
            "required_evidence": ["E-001"],
        }},
    )
    prompt = assemble_prompt(
        prompt_id="P-001", version="0.1", routing_result=routing, context=context
    )
    simulation = execute_simulation(
        prompt, lambda p: {"candidate": "A", "reality_changed": False}, simulation_id="S-001"
    )
    witness = record_simulation_witness(
        witness_id="W-001", prompt=prompt, simulation_result=simulation
    )

    assert witness.witness_id == "W-001"
    assert witness.prompt_id == "P-001"
    assert witness.protocol_id == "protocol.alpha"
    assert witness.simulation_id == "S-001"
    assert witness.evidence_refs == ("E-001", "E-002")
    assert witness.context_version == "1.0"
    assert witness.simulation["kind"] == "simulation"
    assert witness.uncertainty == ("U-001",)


def test_witness_rejects_mismatched_prompt():
    context = {"version": "1.0", "matrix": {"priority": 2, "phase": 1, "relation": 3}}
    routing = route_protocol(context, {"protocol.alpha": {}})
    prompt = assemble_prompt(
        prompt_id="P-001", version="0.1", routing_result=routing, context=context
    )
    simulation = execute_simulation(prompt, lambda p: {"ok": True}, simulation_id="S-001")
    bad = type(simulation)(
        simulation_id="S-001", prompt_id="P-999",
        protocol_id=simulation.protocol_id, status=simulation.status, output=simulation.output
    )

    try:
        record_simulation_witness(
            witness_id="W-002", prompt=prompt, simulation_result=bad
        )
    except ValueError:
        pass
    else:
        raise AssertionError("mismatched prompt must be rejected")

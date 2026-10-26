"""Tests for the Prompt -> Runtime -> Simulation boundary."""

from runtime.prompt import assemble_prompt
from runtime.routing import route_protocol
from runtime.simulation import execute_simulation, capture_simulation_evidence


def _prompt():
    context = {
        "version": "1.0",
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
        "evidence": ["E-001"],
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
    return assemble_prompt(
        prompt_id="P-001",
        version="0.1",
        routing_result=routing,
        context=context,
    )


def test_simulation_result_is_traceable_to_prompt():
    prompt = _prompt()

    result = execute_simulation(
        prompt,
        lambda p: {"answer": "candidate", "reality_changed": False},
        simulation_id="S-001",
    )

    assert result.status == "completed"
    assert result.prompt_id == "P-001"
    assert result.protocol_id == "protocol.alpha"
    assert result.output["reality_changed"] is False


def test_simulation_is_marked_separately_from_reality():
    prompt = _prompt()
    result = execute_simulation(
        prompt,
        lambda p: {"candidate": 42},
        simulation_id="S-002",
    )

    evidence = capture_simulation_evidence(result)

    assert evidence["kind"] == "simulation"
    assert evidence["simulation_id"] == "S-002"


def test_failed_simulation_is_observable():
    prompt = _prompt()

    def failing(_):
        raise RuntimeError("simulation failure")

    result = execute_simulation(prompt, failing, simulation_id="S-003")

    assert result.status == "failed"
    assert result.output["error_type"] == "RuntimeError"

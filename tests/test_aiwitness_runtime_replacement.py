from runtime.aiwitness import record_simulation_witness
from runtime.prompt import PromptSpec
from runtime.simulation import execute_simulation


def test_runtime_replacement_is_visible_to_aiwitness():
    prompt = PromptSpec(
        prompt_id="P-AB-001",
        version="0.1",
        protocol_id="protocol.alpha",
        runtime_target="simulation",
        instructions=("Keep Simulation separate from Reality.",),
        context={"matrix": {"priority": 2, "phase": 1, "relation": 3},
                 "context_version": "1.27"},
        evidence=("E-001", "E-002"),
        uncertainty=("U-001",),
    )

    result_a = execute_simulation(
        prompt,
        lambda p: {"runtime": "A", "candidate": "A1"},
        simulation_id="SIM-A",
    )
    result_b = execute_simulation(
        prompt,
        lambda p: {"runtime": "B", "candidate": "B1"},
        simulation_id="SIM-B",
    )

    witness_a = record_simulation_witness(
        witness_id="W-A",
        prompt=prompt,
        simulation_result=result_a,
    )
    witness_b = record_simulation_witness(
        witness_id="W-B",
        prompt=prompt,
        simulation_result=result_b,
    )

    # The Runtime-specific result remains visible.
    assert witness_a.simulation["output"] != witness_b.simulation["output"]

    # The external meaning boundary remains identical.
    assert witness_a.prompt_id == witness_b.prompt_id == "P-AB-001"
    assert witness_a.protocol_id == witness_b.protocol_id == "protocol.alpha"
    assert witness_a.evidence_refs == witness_b.evidence_refs == ("E-001", "E-002")
    assert witness_a.context_version == witness_b.context_version == "1.27"
    assert witness_a.uncertainty == witness_b.uncertainty == ("U-001",)

    # Replacement is explicit, not hidden.
    assert witness_a.simulation_id != witness_b.simulation_id

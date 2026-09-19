from runtime.prompt import PromptSpec
from runtime.simulation import execute_simulation

def test_runtime_replacement_preserves_external_trace_boundary():
    prompt = PromptSpec(
        prompt_id="P-REPLACE-001",
        version="0.1",
        protocol_id="protocol.alpha",
        runtime_target="simulation",
        instructions=("Treat Evidence references as observed inputs.",),
        context={"matrix": {"priority": 2, "phase": 1, "relation": 3},
                 "context_version": "1.27"},
        evidence=("E-001", "E-002"),
        uncertainty=("U-001",),
    )

    def runtime_a(p):
        return {"provider": "A", "candidate": "A1"}

    def runtime_b(p):
        return {"provider": "B", "candidate": "B1"}

    result_a = execute_simulation(prompt, runtime_a, simulation_id="SIM-A")
    result_b = execute_simulation(prompt, runtime_b, simulation_id="SIM-B")

    assert result_a.status == result_b.status == "completed"
    assert result_a.prompt_id == result_b.prompt_id == "P-REPLACE-001"
    assert result_a.protocol_id == result_b.protocol_id == "protocol.alpha"
    assert result_a.output != result_b.output

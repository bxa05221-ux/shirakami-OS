from runtime.aiwitness import record_simulation_witness
from runtime.operation import HumanDecision, authorize_operation
from runtime.prompt import PromptSpec
from runtime.reconstruction import reconstruct_trace
from runtime.simulation import execute_simulation


def test_runtime_a_both_reach_human_decision_operation_reconstruction():
    prompt = PromptSpec(
        prompt_id="P-AB-ROUNDTRIP-001",
        version="0.1",
        protocol_id="protocol.alpha",
        runtime_target="simulation",
        instructions=("Keep Simulation separate from Reality.",),
        context={"matrix": {"priority": 2, "phase": 1, "relation": 3},
                 "context_version": "1.27"},
        evidence=("E-001", "E-002"),
        uncertainty=("U-001",),
    )

    runtimes = {
        "A": ("SIM-A", "W-A", "D-A", "OP-A", "E-003A"),
        "B": ("SIM-B", "W-B", "D-B", "OP-B", "E-003B"),
    }

    traces = {}
    for runtime_name, (simulation_id, witness_id, decision_id, operation_id, resulting_evidence) in runtimes.items():
        simulation = execute_simulation(
            prompt,
            lambda p, name=runtime_name: {
                "runtime": name,
                "candidate": f"{name}-candidate",
            },
            simulation_id=simulation_id,
        )
        witness = record_simulation_witness(
            witness_id=witness_id,
            prompt=prompt,
            simulation_result=simulation,
        )
        decision = HumanDecision(
            decision_id=decision_id,
            simulation_id=simulation.simulation_id,
            status="approved",
            decided_by="human-001",
            rationale=f"explicit human approval for Runtime {runtime_name}",
        )
        operation = authorize_operation(
            decision=decision,
            simulation=simulation,
            operation_id=operation_id,
            operation=lambda s, evidence=resulting_evidence: {
                "reality_changed": True,
                "result": evidence,
            },
        )
        traces[runtime_name] = reconstruct_trace(
            witness=witness,
            decision=decision,
            operation=operation,
            resulting_evidence_refs=(resulting_evidence,),
        )

    trace_a = traces["A"]
    trace_b = traces["B"]

    # Both runtimes complete the same external lifecycle.
    assert trace_a.decision_status == trace_b.decision_status == "approved"
    assert trace_a.operation_status == trace_b.operation_status == "completed"
    assert trace_a.reality_changed is trace_b.reality_changed is True

    # Shared external meaning boundary.
    assert trace_a.prompt_id == trace_b.prompt_id == "P-AB-ROUNDTRIP-001"
    assert trace_a.protocol_id == trace_b.protocol_id == "protocol.alpha"
    assert trace_a.input_evidence_refs == trace_b.input_evidence_refs == ("E-001", "E-002")
    assert trace_a.context_version == trace_b.context_version == "1.27"

    # Runtime-specific provenance remains distinct.
    assert trace_a.simulation_id != trace_b.simulation_id
    assert trace_a.witness_id != trace_b.witness_id
    assert trace_a.decision_id != trace_b.decision_id
    assert trace_a.operation_id != trace_b.operation_id
    assert trace_a.resulting_evidence_refs != trace_b.resulting_evidence_refs

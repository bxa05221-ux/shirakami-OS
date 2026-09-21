from dataclasses import replace

from runtime.aiwitness import record_simulation_witness
from runtime.integrity import classify_trace_integrity
from runtime.integrity_reconstruction import reconstruct_integrity
from runtime.operation import HumanDecision, authorize_operation
from runtime.prompt import assemble_prompt
from runtime.reconstruction import reconstruct_trace
from runtime.routing import route_protocol
from runtime.simulation import execute_simulation


def _full_chain():
    context = {
        "version": "1.27",
        "evidence": ("E-001", "E-002"),
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
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
        prompt_id="P-0043",
        version="0.1",
        routing_result=routing,
        context=context,
    )
    simulation = execute_simulation(
        prompt, lambda p: {"candidate": "A"}, simulation_id="SIM-0043"
    )
    witness = record_simulation_witness(
        witness_id="W-0043",
        prompt=prompt,
        simulation_result=simulation,
    )
    decision = HumanDecision(
        decision_id="D-0043",
        simulation_id=simulation.simulation_id,
        status="approved",
        decided_by="human-0043",
    )
    operation = authorize_operation(
        decision=decision,
        simulation=simulation,
        operation_id="OP-0043",
        operation=lambda s: {"reality_changed": True},
    )
    trace = reconstruct_trace(
        witness=witness,
        decision=decision,
        operation=operation,
        resulting_evidence_refs=("E-003",),
    )
    return context, prompt, simulation, witness, decision, operation, trace


def test_clean_trace_has_no_integrity_findings():
    _, _, simulation, witness, decision, operation, trace = _full_chain()

    findings = classify_trace_integrity(
        simulation=simulation,
        witness=witness,
        decision=decision,
        operation=operation,
        trace=trace,
        expected_context_version="1.27",
    )

    assert findings == ()


def test_tampered_trace_round_trips_as_integrity_evidence():
    _, _, simulation, witness, decision, operation, trace = _full_chain()
    tampered = replace(decision, simulation_id="SIM-TAMPERED")

    findings = classify_trace_integrity(
        simulation=simulation,
        witness=witness,
        decision=tampered,
        operation=operation,
        trace=trace,
    )

    codes = {item.code for item in findings}
    assert "DECISION_SIMULATION_MISMATCH" in codes
    assert "DECISION_OPERATION_MISMATCH" in codes

    reconstruction = reconstruct_integrity(
        reconstruction_id="IR-0043",
        trace=trace,
        findings=findings,
    )

    assert reconstruction.status == "integrity_findings_present"
    assert {item.code for item in reconstruction.findings} == codes
    assert reconstruction.trace_identity[0] == "W-0043"

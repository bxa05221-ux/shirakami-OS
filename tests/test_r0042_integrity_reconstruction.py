from dataclasses import replace

from runtime.aiwitness import record_simulation_witness
from runtime.integrity import classify_trace_integrity
from runtime.integrity_reconstruction import (
    integrity_reconstruction_as_evidence,
    reconstruct_integrity,
)
from runtime.operation import HumanDecision, authorize_operation
from runtime.prompt import assemble_prompt
from runtime.reconstruction import reconstruct_trace
from runtime.routing import route_protocol
from runtime.simulation import execute_simulation


def _chain():
    context = {
        "version": "1.27",
        "evidence": ("E-001", "E-002"),
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
    }
    routing = route_protocol(
        context,
        {
            "protocol.alpha": {
                "accepted_states": [
                    {"priority": 2, "phase": 1, "relation": 3}
                ],
                "required_evidence": ["E-001"],
            }
        },
    )
    prompt = assemble_prompt(
        prompt_id="P-0042",
        version="0.1",
        routing_result=routing,
        context=context,
    )
    simulation = execute_simulation(
        prompt, lambda p: {"candidate": "A"}, simulation_id="SIM-0042"
    )
    witness = record_simulation_witness(
        witness_id="W-0042",
        prompt=prompt,
        simulation_result=simulation,
    )
    decision = HumanDecision(
        decision_id="D-0042",
        simulation_id=simulation.simulation_id,
        status="approved",
        decided_by="human-0042",
    )
    operation = authorize_operation(
        decision=decision,
        simulation=simulation,
        operation_id="OP-0042",
        operation=lambda s: {"reality_changed": True},
    )
    trace = reconstruct_trace(
        witness=witness,
        decision=decision,
        operation=operation,
        resulting_evidence_refs=("E-003",),
    )
    return context, prompt, simulation, witness, decision, operation, trace


def test_integrity_failure_can_be_reconstructed_without_inventing_cause():
    _, _, simulation, witness, decision, operation, trace = _chain()
    tampered_witness = replace(witness, context_version="9.99")
    findings = classify_trace_integrity(
        witness=tampered_witness,
        expected_context_version="1.27",
    )

    reconstruction = reconstruct_integrity(
        reconstruction_id="IR-0042",
        trace=trace,
        findings=findings,
    )

    assert reconstruction.status == "integrity_findings_present"
    assert reconstruction.trace_identity == (
        "W-0042",
        "P-0042",
        "protocol.alpha",
        "SIM-0042",
        "D-0042",
        "OP-0042",
    )
    assert reconstruction.context_version == "1.27"
    assert reconstruction.findings[0].code == "CONTEXT_TAMPERED"


def test_integrity_reconstruction_preserves_empty_result_evidence():
    _, _, _, witness, decision, operation, _ = _chain()
    trace = reconstruct_trace(
        witness=witness,
        decision=decision,
        operation=operation,
    )
    findings = classify_trace_integrity(trace=trace)

    assert "RESULT_EVIDENCE_MISSING" in {item.code for item in findings}

    reconstruction = reconstruct_integrity(
        reconstruction_id="IR-EMPTY-EVIDENCE",
        trace=trace,
        findings=findings,
    )
    assert reconstruction.findings[0].code == "RESULT_EVIDENCE_MISSING"


def test_integrity_reconstruction_requires_observable_input():
    try:
        reconstruct_integrity(
            reconstruction_id="IR-NONE",
            trace=None,
            findings=(),
        )
    except ValueError as exc:
        assert "requires trace or findings" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_integrity_reconstruction_is_evidence_shaped():
    _, _, _, _, _, _, trace = _chain()
    findings = classify_trace_integrity(trace=trace)
    reconstruction = reconstruct_integrity(
        reconstruction_id="IR-EVIDENCE",
        trace=trace,
        findings=findings,
    )
    evidence = integrity_reconstruction_as_evidence(reconstruction)

    assert evidence["kind"] == "integrity_reconstruction"
    assert evidence["reconstruction_id"] == "IR-EVIDENCE"
    assert "findings" in evidence

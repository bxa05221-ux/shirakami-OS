from dataclasses import replace

from runtime.aiwitness import record_simulation_witness
from runtime.integrity import classify_trace_integrity, findings_as_evidence
from runtime.operation import HumanDecision, authorize_operation
from runtime.prompt import assemble_prompt
from runtime.reconstruction import reconstruct_trace
from runtime.routing import route_protocol
from runtime.simulation import execute_simulation


def _ready_chain():
    context = {
        "version": "1.27",
        "evidence": ("E-001", "E-002"),
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
    }
    protocols = {
        "protocol.alpha": {
            "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
            "required_evidence": ["E-001"],
        }
    }
    routing = route_protocol(context, protocols)
    prompt = assemble_prompt(
        prompt_id="P-0041",
        version="0.1",
        routing_result=routing,
        context=context,
    )
    simulation = execute_simulation(
        prompt, lambda p: {"candidate": "A"}, simulation_id="SIM-0041"
    )
    witness = record_simulation_witness(
        witness_id="W-0041",
        prompt=prompt,
        simulation_result=simulation,
    )
    decision = HumanDecision(
        decision_id="D-0041",
        simulation_id=simulation.simulation_id,
        status="approved",
        decided_by="human-0041",
    )
    operation = authorize_operation(
        decision=decision,
        simulation=simulation,
        operation_id="OP-0041",
        operation=lambda s: {"reality_changed": True, "result": "E-003"},
    )
    trace = reconstruct_trace(
        witness=witness,
        decision=decision,
        operation=operation,
        resulting_evidence_refs=("E-003",),
    )
    return context, routing, prompt, simulation, witness, decision, operation, trace


def _codes(findings):
    return {item.code for item in findings}


def test_classifies_missing_evidence():
    context, *_ = _ready_chain()
    blocked = route_protocol(
        context,
        {
            "protocol.alpha": {
                "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
                "required_evidence": ["E-MISSING"],
            }
        },
    )

    assert _codes(classify_trace_integrity(routing=blocked)) == {"EVIDENCE_MISSING"}


def test_classifies_prompt_simulation_mismatch():
    _, _, prompt, simulation, *_ = _ready_chain()
    crossed = replace(simulation, prompt_id="P-OTHER")

    assert "PROMPT_SIMULATION_MISMATCH" in _codes(
        classify_trace_integrity(prompt=prompt, simulation=crossed)
    )


def test_classifies_decision_simulation_mismatch_and_missing_approval():
    _, _, _, simulation, _, decision, *_ = _ready_chain()
    crossed = replace(decision, simulation_id="SIM-OTHER", status="rejected")

    codes = _codes(
        classify_trace_integrity(decision=crossed, simulation=simulation)
    )
    assert codes == {"DECISION_SIMULATION_MISMATCH", "HUMAN_APPROVAL_MISSING"}


def test_classifies_context_tampering():
    _, _, _, _, witness, *_ = _ready_chain()
    tampered = replace(witness, context_version="9.99")

    assert "CONTEXT_TAMPERED" in _codes(
        classify_trace_integrity(
            witness=tampered,
            expected_context_version="1.27",
        )
    )


def test_classifies_missing_result_evidence():
    _, _, _, _, witness, decision, operation, _ = _ready_chain()
    trace = reconstruct_trace(
        witness=witness,
        decision=decision,
        operation=operation,
    )

    assert "RESULT_EVIDENCE_MISSING" in _codes(
        classify_trace_integrity(trace=trace)
    )


def test_classifies_runtime_failure():
    _, _, prompt, *_ = _ready_chain()
    failed = execute_simulation(
        prompt,
        lambda p: (_ for _ in ()).throw(RuntimeError("intentional failure")),
        simulation_id="SIM-FAIL-0041",
    )

    assert "RUNTIME_FAILURE" in _codes(
        classify_trace_integrity(simulation=failed)
    )


def test_findings_can_be_preserved_as_evidence():
    finding = classify_trace_integrity(
        routing=route_protocol(
            {"evidence": (), "matrix": {"priority": 2, "phase": 1, "relation": 3}},
            {
                "protocol.alpha": {
                    "accepted_states": [
                        {"priority": 2, "phase": 1, "relation": 3}
                    ],
                    "required_evidence": ["E-MISSING"],
                }
            },
        )
    )

    evidence = findings_as_evidence(finding)

    assert evidence["kind"] == "trace_integrity_findings"
    assert evidence["findings"][0]["code"] == "EVIDENCE_MISSING"

from runtime.aiwitness import record_simulation_witness
from runtime.operation import HumanDecision, authorize_operation
from runtime.prompt import assemble_prompt
from runtime.reconstruction import reconstruct_trace
from runtime.routing import route_protocol
from runtime.simulation import execute_simulation


def test_full_shirakami_trace_round_trip():
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
    assert routing.status == "ready"
    assert routing.selected_protocol == "protocol.alpha"

    prompt = assemble_prompt(
        prompt_id="P-001",
        version="0.1",
        routing_result=routing,
        context=context,
    )

    simulation = execute_simulation(
        prompt,
        lambda p: {"candidate": "A", "evidence_count": len(p.evidence)},
        simulation_id="SIM-001",
    )
    assert simulation.status == "completed"

    witness = record_simulation_witness(
        witness_id="W-001",
        prompt=prompt,
        simulation_result=simulation,
    )

    decision = HumanDecision(
        decision_id="D-001",
        simulation_id=simulation.simulation_id,
        status="approved",
        decided_by="human-001",
        rationale="explicit human approval",
    )

    operation = authorize_operation(
        decision=decision,
        simulation=simulation,
        operation_id="OP-001",
        operation=lambda s: {
            "reality_changed": True,
            "result": "E-003",
        },
    )
    assert operation.status == "completed"
    assert operation.reality_changed is True

    trace = reconstruct_trace(
        witness=witness,
        decision=decision,
        operation=operation,
        resulting_evidence_refs=("E-003",),
    )

    assert trace.input_evidence_refs == ("E-001", "E-002")
    assert trace.resulting_evidence_refs == ("E-003",)
    assert trace.context_version == "1.27"
    assert trace.witness_id == "W-001"
    assert trace.prompt_id == "P-001"
    assert trace.protocol_id == "protocol.alpha"
    assert trace.simulation_id == "SIM-001"
    assert trace.decision_id == "D-001"
    assert trace.operation_id == "OP-001"

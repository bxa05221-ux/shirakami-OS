from dataclasses import replace

import pytest

from runtime.aiwitness import record_simulation_witness
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
        prompt_id="P-0040",
        version="0.1",
        routing_result=routing,
        context=context,
    )
    simulation = execute_simulation(
        prompt,
        lambda p: {"candidate": "A"},
        simulation_id="SIM-0040",
    )
    witness = record_simulation_witness(
        witness_id="W-0040",
        prompt=prompt,
        simulation_result=simulation,
    )
    decision = HumanDecision(
        decision_id="D-0040",
        simulation_id=simulation.simulation_id,
        status="approved",
        decided_by="human-0040",
    )
    operation = authorize_operation(
        decision=decision,
        simulation=simulation,
        operation_id="OP-0040",
        operation=lambda s: {"reality_changed": True, "result": "E-003"},
    )
    trace = reconstruct_trace(
        witness=witness,
        decision=decision,
        operation=operation,
        resulting_evidence_refs=("E-003",),
    )
    return context, routing, prompt, simulation, witness, decision, operation, trace


def test_missing_evidence_blocks_routing():
    context, *_ = _ready_chain()
    protocols = {
        "protocol.alpha": {
            "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
            "required_evidence": ["E-MISSING"],
        }
    }

    result = route_protocol(context, protocols)

    assert result.status == "blocked"
    assert result.selected_protocol is None


def test_blocked_routing_cannot_be_turned_into_prompt():
    context, *_ = _ready_chain()
    protocols = {
        "protocol.alpha": {
            "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
            "required_evidence": ["E-MISSING"],
        }
    }
    blocked = route_protocol(context, protocols)

    with pytest.raises(ValueError):
        assemble_prompt(
            prompt_id="P-BLOCKED",
            version="0.1",
            routing_result=blocked,
            context=context,
        )


def test_crossed_prompt_and_simulation_are_rejected_by_witness():
    _, _, prompt, simulation, *_ = _ready_chain()
    crossed = replace(simulation, prompt_id="P-TAMPERED")

    with pytest.raises(ValueError):
        record_simulation_witness(
            witness_id="W-TAMPERED",
            prompt=prompt,
            simulation_result=crossed,
        )


def test_crossed_decision_and_simulation_are_rejected_by_operation():
    _, _, _, simulation, _, decision, *_ = _ready_chain()
    crossed = replace(decision, simulation_id="SIM-OTHER")

    with pytest.raises(ValueError):
        authorize_operation(
            decision=crossed,
            simulation=simulation,
            operation_id="OP-TAMPERED",
            operation=lambda s: {"reality_changed": True},
        )


def test_unapproved_human_decision_cannot_execute_operation():
    _, _, _, simulation, _, decision, *_ = _ready_chain()
    rejected = replace(decision, status="rejected")

    with pytest.raises(ValueError):
        authorize_operation(
            decision=rejected,
            simulation=simulation,
            operation_id="OP-REJECTED",
            operation=lambda s: {"reality_changed": True},
        )


def test_crossed_decision_and_operation_are_rejected_by_reconstruction():
    _, _, _, simulation, witness, decision, operation, _ = _ready_chain()
    crossed = replace(decision, simulation_id="SIM-OTHER")

    with pytest.raises(ValueError):
        reconstruct_trace(
            witness=witness,
            decision=crossed,
            operation=operation,
            resulting_evidence_refs=("E-003",),
        )


def test_missing_resulting_evidence_is_not_invented():
    _, _, _, _, witness, decision, operation, _ = _ready_chain()

    trace = reconstruct_trace(
        witness=witness,
        decision=decision,
        operation=operation,
    )

    assert trace.resulting_evidence_refs == ()


def test_tampered_context_version_remains_observable():
    _, _, prompt, simulation, witness, decision, operation, _ = _ready_chain()
    tampered_prompt = replace(
        prompt,
        context={**prompt.context, "context_version": "9.99"},
    )

    tampered_witness = record_simulation_witness(
        witness_id="W-CONTEXT-TAMPERED",
        prompt=tampered_prompt,
        simulation_result=simulation,
    )

    trace = reconstruct_trace(
        witness=tampered_witness,
        decision=decision,
        operation=operation,
        resulting_evidence_refs=("E-003",),
    )

    assert trace.context_version == "9.99"


def test_runtime_failure_is_observable_and_cannot_claim_reality_change():
    _, _, prompt, _, *_ = _ready_chain()

    result = execute_simulation(
        prompt,
        lambda p: (_ for _ in ()).throw(RuntimeError("intentional failure")),
        simulation_id="SIM-FAIL",
    )

    assert result.status == "failed"
    assert result.output["error_type"] == "RuntimeError"

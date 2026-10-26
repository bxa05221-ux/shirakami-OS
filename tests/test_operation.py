"""Tests for the Human Decision -> Operation boundary."""

from runtime.routing import route_protocol
from runtime.prompt import assemble_prompt
from runtime.simulation import execute_simulation
from runtime.operation import HumanDecision, authorize_operation


def _simulation():
    context = {
        "version": "1.0",
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
        "evidence": ["E-001"],
    }
    routing = route_protocol(context, {"protocol.alpha": {}})
    prompt = assemble_prompt(
        prompt_id="P-001", version="0.1", routing_result=routing, context=context
    )
    return execute_simulation(
        prompt, lambda p: {"candidate": "A"}, simulation_id="S-001"
    )


def test_operation_requires_explicit_human_approval():
    simulation = _simulation()
    decision = HumanDecision(
        decision_id="D-001", simulation_id="S-001", status="approved", decided_by="human"
    )
    result = authorize_operation(
        decision=decision,
        simulation=simulation,
        operation_id="O-001",
        operation=lambda s: {"executed": True, "reality_changed": True},
    )
    assert result.status == "completed"
    assert result.reality_changed is True
    assert result.decision_id == "D-001"


def test_unapproved_decision_cannot_execute_operation():
    simulation = _simulation()
    decision = HumanDecision(
        decision_id="D-002", simulation_id="S-001", status="rejected", decided_by="human"
    )
    try:
        authorize_operation(
            decision=decision,
            simulation=simulation,
            operation_id="O-002",
            operation=lambda s: {"executed": True},
        )
    except ValueError:
        pass
    else:
        raise AssertionError("unapproved operation must be rejected")


def test_operation_failure_is_observable():
    simulation = _simulation()
    decision = HumanDecision(
        decision_id="D-003", simulation_id="S-001", status="approved", decided_by="human"
    )

    def failing(_):
        raise RuntimeError("operation failure")

    result = authorize_operation(
        decision=decision,
        simulation=simulation,
        operation_id="O-003",
        operation=failing,
    )
    assert result.status == "failed"
    assert result.reality_changed is False

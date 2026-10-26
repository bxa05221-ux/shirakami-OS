from runtime.aiwitness import WitnessRecord
from runtime.operation import HumanDecision, OperationResult
from runtime.reconstruction import reconstruct_trace, trace_as_evidence


def make_witness() -> WitnessRecord:
    return WitnessRecord(
        witness_id="W-001",
        prompt_id="P-001",
        protocol_id="protocol.alpha",
        simulation_id="SIM-001",
        evidence_refs=("E-001", "E-002"),
        context_version="1.27",
        simulation_status="completed",
        observation={"kind": "input_references"},
        simulation={"kind": "simulation", "output": {"candidate": "A"}},
        uncertainty=("U-001",),
    )


def make_decision() -> HumanDecision:
    return HumanDecision(
        decision_id="D-001",
        simulation_id="SIM-001",
        status="approved",
        decided_by="human-001",
        rationale="explicit approval",
    )


def test_reconstructs_complete_chain():
    trace = reconstruct_trace(
        witness=make_witness(),
        decision=make_decision(),
        operation=OperationResult(
            operation_id="OP-001",
            decision_id="D-001",
            simulation_id="SIM-001",
            status="completed",
            reality_changed=True,
            output={"reality_changed": True},
        ),
        resulting_evidence_refs=("E-003",),
    )

    assert trace.input_evidence_refs == ("E-001", "E-002")
    assert trace.resulting_evidence_refs == ("E-003",)
    assert trace.decision_id == "D-001"
    assert trace.operation_id == "OP-001"
    assert trace.reality_changed is True


def test_reconstruction_rejects_crossed_simulation():
    decision = HumanDecision(
        decision_id="D-002",
        simulation_id="SIM-OTHER",
        status="approved",
        decided_by="human-001",
    )

    try:
        reconstruct_trace(
            witness=make_witness(),
            decision=decision,
            operation=OperationResult(
                operation_id="OP-002",
                decision_id="D-002",
                simulation_id="SIM-OTHER",
                status="completed",
                reality_changed=False,
                output={},
            ),
        )
    except ValueError as exc:
        assert "witness and decision" in str(exc)
    else:
        raise AssertionError("crossed simulation must be rejected")


def test_trace_does_not_invent_resulting_evidence():
    trace = reconstruct_trace(
        witness=make_witness(),
        decision=make_decision(),
        operation=OperationResult(
            operation_id="OP-003",
            decision_id="D-001",
            simulation_id="SIM-001",
            status="completed",
            reality_changed=False,
            output={},
        ),
    )

    assert trace.resulting_evidence_refs == ()
    serialized = trace_as_evidence(trace)
    assert serialized["resulting_evidence_refs"] == ()

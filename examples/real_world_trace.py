"""Concrete reconstructable incident example using the Shirakami runtime boundary.

Scenario: a refrigerated storage unit reports an abnormal temperature.
The AI only simulates options; a human explicitly authorizes the operation.
"""

from runtime.aiwitness import record_simulation_witness
from runtime.operation import HumanDecision, authorize_operation
from runtime.prompt import assemble_prompt
from runtime.reconstruction import reconstruct_trace
from runtime.routing import route_protocol
from runtime.simulation import execute_simulation


def run_example():
    context = {
        "version": "demo-1.0",
        "evidence": ("TEMP-2026-09-19-001", "STOCK-2026-09-19-001"),
        "matrix": {"priority": 2, "phase": 1, "relation": 3},
    }

    protocols = {
        "cold-storage-check": {
            "accepted_states": [{"priority": 2, "phase": 1, "relation": 3}],
            "required_evidence": ["TEMP-2026-09-19-001"],
        }
    }

    routing = route_protocol(context, protocols)
    prompt = assemble_prompt(
        prompt_id="P-DEMO-001",
        version="1.0",
        routing_result=routing,
        context=context,
        uncertainty=("Sensor reading is abnormal; cause is not established.",),
    )

    simulation = execute_simulation(
        prompt,
        lambda p: {
            "candidate_actions": ["verify sensor", "inspect storage unit"],
            "recommendation": "human review required",
        },
        simulation_id="SIM-DEMO-001",
    )

    witness = record_simulation_witness(
        witness_id="W-DEMO-001",
        prompt=prompt,
        simulation_result=simulation,
    )

    decision = HumanDecision(
        decision_id="D-DEMO-001",
        simulation_id=simulation.simulation_id,
        status="approved",
        decided_by="human-operator",
        rationale="Authorize inspection after reviewing the simulation.",
    )

    operation = authorize_operation(
        decision=decision,
        simulation=simulation,
        operation_id="OP-DEMO-001",
        operation=lambda _: {
            "reality_changed": False,
            "result": "inspection requested; no automated equipment change",
        },
    )

    trace = reconstruct_trace(
        witness=witness,
        decision=decision,
        operation=operation,
        resulting_evidence_refs=("INSPECTION-2026-09-19-001",),
    )

    return {
        "routing": routing,
        "prompt": prompt,
        "simulation": simulation,
        "witness": witness,
        "decision": decision,
        "operation": operation,
        "trace": trace,
    }


if __name__ == "__main__":
    result = run_example()
    print("status:", result["operation"].status)
    print("selected_protocol:", result["routing"].selected_protocol)
    print("simulation:", result["simulation"].output)
    print("human_decision:", result["decision"].status)
    print("reconstructed:", result["trace"].input_evidence_refs, "->", result["trace"].resulting_evidence_refs)

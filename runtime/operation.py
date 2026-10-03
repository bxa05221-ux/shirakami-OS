"""Human decision and operation boundary for Shirakami MVP.

A Simulation may propose a candidate, but only an explicit HumanDecision can
authorize an Operation. The operation result is observable and does not imply
that Reality was changed unless an external adapter reports that fact.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .simulation import SimulationResult


@dataclass(frozen=True)
class HumanDecision:
    decision_id: str
    simulation_id: str
    status: str
    decided_by: str
    rationale: str = ""


@dataclass(frozen=True)
class OperationResult:
    operation_id: str
    decision_id: str
    simulation_id: str
    status: str
    reality_changed: bool
    output: Mapping[str, Any]


Operation = Any


def authorize_operation(
    *,
    decision: HumanDecision,
    simulation: SimulationResult,
    operation_id: str,
    operation: Operation,
) -> OperationResult:
    """Execute an operation only after an explicit human authorization."""
    if decision.simulation_id != simulation.simulation_id:
        raise ValueError("decision and simulation result do not match")
    if decision.status != "approved":
        raise ValueError("operation requires an approved human decision")
    if not callable(operation):
        raise TypeError("operation must be callable")

    try:
        output = operation(simulation)
    except Exception as exc:
        return OperationResult(
            operation_id=operation_id,
            decision_id=decision.decision_id,
            simulation_id=simulation.simulation_id,
            status="failed",
            reality_changed=False,
            output={"error_type": type(exc).__name__, "message": str(exc)},
        )

    if not isinstance(output, Mapping):
        return OperationResult(
            operation_id=operation_id,
            decision_id=decision.decision_id,
            simulation_id=simulation.simulation_id,
            status="failed",
            reality_changed=False,
            output={"error_type": "InvalidOperationResult"},
        )

    return OperationResult(
        operation_id=operation_id,
        decision_id=decision.decision_id,
        simulation_id=simulation.simulation_id,
        status="completed",
        reality_changed=bool(output.get("reality_changed", False)),
        output=dict(output),
    )

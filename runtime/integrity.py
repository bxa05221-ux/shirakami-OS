"""Adversarial trace-integrity classification for Shirakami MVP.

This layer classifies observable integrity failures. It does not repair records,
infer missing facts, or make human decisions.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .aiwitness import WitnessRecord
from .operation import HumanDecision, OperationResult
from .reconstruction import ReconstructionTrace
from .routing import RoutingResult
from .simulation import SimulationResult


@dataclass(frozen=True)
class IntegrityFinding:
    code: str
    severity: str
    detail: str


def classify_trace_integrity(
    *,
    routing: RoutingResult | None = None,
    prompt: Any | None = None,
    simulation: SimulationResult | None = None,
    witness: WitnessRecord | None = None,
    decision: HumanDecision | None = None,
    operation: OperationResult | None = None,
    trace: ReconstructionTrace | None = None,
    expected_context_version: str | None = None,
) -> tuple[IntegrityFinding, ...]:
    """Return deterministic classifications for observable trace failures."""
    findings: list[IntegrityFinding] = []

    if routing is not None and routing.status != "ready":
        findings.append(
            IntegrityFinding(
                "EVIDENCE_MISSING",
                "error",
                "routing is blocked; required Evidence is unavailable",
            )
        )

    if prompt is not None and simulation is not None:
        if prompt.prompt_id != simulation.prompt_id:
            findings.append(
                IntegrityFinding(
                    "PROMPT_SIMULATION_MISMATCH",
                    "error",
                    "Prompt and Simulation identifiers differ",
                )
            )
        if prompt.protocol_id != simulation.protocol_id:
            findings.append(
                IntegrityFinding(
                    "PROTOCOL_SIMULATION_MISMATCH",
                    "error",
                    "Protocol and Simulation identifiers differ",
                )
            )

    if witness is not None and simulation is not None:
        if witness.simulation_id != simulation.simulation_id:
            findings.append(
                IntegrityFinding(
                    "WITNESS_SIMULATION_MISMATCH",
                    "error",
                    "AIwitness and Simulation identifiers differ",
                )
            )

    if decision is not None and simulation is not None:
        if decision.simulation_id != simulation.simulation_id:
            findings.append(
                IntegrityFinding(
                    "DECISION_SIMULATION_MISMATCH",
                    "error",
                    "HumanDecision and Simulation identifiers differ",
                )
            )
        if decision.status != "approved":
            findings.append(
                IntegrityFinding(
                    "HUMAN_APPROVAL_MISSING",
                    "error",
                    "operation lacks explicit human approval",
                )
            )

    if operation is not None and decision is not None:
        if operation.decision_id != decision.decision_id:
            findings.append(
                IntegrityFinding(
                    "DECISION_OPERATION_MISMATCH",
                    "error",
                    "HumanDecision and Operation identifiers differ",
                )
            )

    if witness is not None and expected_context_version is not None:
        if witness.context_version != expected_context_version:
            findings.append(
                IntegrityFinding(
                    "CONTEXT_TAMPERED",
                    "error",
                    "observed context version differs from expected version",
                )
            )

    if simulation is not None and simulation.status == "failed":
        findings.append(
            IntegrityFinding(
                "RUNTIME_FAILURE",
                "error",
                "Simulation Runtime reported a failed observable result",
            )
        )

    if trace is not None:
        if trace.reality_changed and not trace.resulting_evidence_refs:
            findings.append(
                IntegrityFinding(
                    "RESULT_EVIDENCE_MISSING",
                    "error",
                    "trace reports Reality change without resulting Evidence reference",
                )
            )

    return tuple(findings)


def findings_as_evidence(findings: tuple[IntegrityFinding, ...]) -> Mapping[str, Any]:
    """Serialize classifications without turning them into inferred facts."""
    return {
        "kind": "trace_integrity_findings",
        "findings": tuple(
            {
                "code": item.code,
                "severity": item.severity,
                "detail": item.detail,
            }
            for item in findings
        ),
    }
}

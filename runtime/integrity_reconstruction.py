"""Reconstruction of observable integrity failures.

R0042 turns integrity findings into an explicit reconstruction record. It does
not repair the trace, infer hidden causes, or make a human decision.
"""

from dataclasses import dataclass
from typing import Any, Mapping

from .integrity import IntegrityFinding
from .reconstruction import ReconstructionTrace


@dataclass(frozen=True)
class IntegrityReconstruction:
    reconstruction_id: str
    trace_identity: tuple[str, ...]
    context_version: str | None
    findings: tuple[IntegrityFinding, ...]
    status: str


def reconstruct_integrity(
    *,
    reconstruction_id: str,
    trace: ReconstructionTrace | None,
    findings: tuple[IntegrityFinding, ...],
) -> IntegrityReconstruction:
    """Preserve the observable relationship between a trace and its findings."""
    if trace is None and not findings:
        raise ValueError("integrity reconstruction requires trace or findings")

    identity: tuple[str, ...] = ()
    context_version = None
    if trace is not None:
        identity = (
            trace.witness_id,
            trace.prompt_id,
            trace.protocol_id,
            trace.simulation_id,
            trace.decision_id,
            trace.operation_id,
        )
        context_version = trace.context_version

    return IntegrityReconstruction(
        reconstruction_id=reconstruction_id,
        trace_identity=identity,
        context_version=context_version,
        findings=tuple(findings),
        status="integrity_findings_present" if findings else "no_integrity_findings",
    )


def integrity_reconstruction_as_evidence(
    reconstruction: IntegrityReconstruction,
) -> Mapping[str, Any]:
    """Serialize the reconstruction as Evidence without adding causal claims."""
    return {
        "kind": "integrity_reconstruction",
        "reconstruction_id": reconstruction.reconstruction_id,
        "trace_identity": reconstruction.trace_identity,
        "context_version": reconstruction.context_version,
        "status": reconstruction.status,
        "findings": tuple(
            {
                "code": item.code,
                "severity": item.severity,
                "detail": item.detail,
            }
            for item in reconstruction.findings
        ),
    }

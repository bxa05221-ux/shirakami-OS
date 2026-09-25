"""Machine-checkable provenance chain for Shirakami execution observations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TraceabilityRecord:
    """A normalized link across Evidence, Handoff, Execution, Trace and Witness."""

    evidence_ids: tuple[str, ...]
    handoff_id: str
    execution_id: str
    trace_id: str
    witness_id: str
    verification_status: str
    commit: str | None
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False
    human_gate_required: bool = True


def validate_traceability(
    *,
    trace: dict,
    witness: dict,
    execution: dict,
    evidence_ids: Iterable[str],
) -> TraceabilityRecord:
    """Validate identity continuity without inferring authority."""

    expected_evidence = tuple(evidence_ids)
    if tuple(trace.get("evidence_ids", ())) != expected_evidence:
        raise ValueError("trace evidence_ids do not match expected evidence")
    if tuple(witness.get("evidence_ids", ())) != expected_evidence:
        raise ValueError("witness evidence_ids do not match expected evidence")
    if execution.get("evidence_ids", []) != list(expected_evidence):
        raise ValueError("execution evidence_ids do not match expected evidence")

    for field in ("handoff_id", "execution_id", "trace_id"):
        if trace.get(field) != execution.get(field):
            raise ValueError(f"{field} mismatch between trace and execution")
    for field in ("trace_id", "execution_id", "handoff_id"):
        if witness.get(field) != trace.get(field):
            raise ValueError(f"{field} mismatch between witness and trace")

    if witness.get("verification_status") != trace.get("verification_status"):
        raise ValueError("verification status mismatch between witness and trace")
    if witness.get("commit") != trace.get("commit"):
        raise ValueError("commit mismatch between witness and trace")

    for record_name, record in (
        ("trace", trace),
        ("witness", witness),
        ("execution", execution),
    ):
        if record.get("execution_authorized") is not False:
            raise ValueError(f"{record_name} grants execution authority")
        if record.get("publish_authorized") is not False:
            raise ValueError(f"{record_name} grants publish authority")
        if record.get("merge_authorized") is not False:
            raise ValueError(f"{record_name} grants merge authority")
        if record.get("human_gate_required") is not True:
            raise ValueError(f"{record_name} must require human gate")

    return TraceabilityRecord(
        evidence_ids=expected_evidence,
        handoff_id=str(trace["handoff_id"]),
        execution_id=str(trace["execution_id"]),
        trace_id=str(trace["trace_id"]),
        witness_id=str(witness["witness_id"]),
        verification_status=str(trace["verification_status"]),
        commit=trace.get("commit"),
    )

"""Deterministic replay boundary for Runtime β0.1.

Replay observes existing execution artifacts. It does not introduce protocol
semantics or mutate Evidence records.
"""

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Mapping

from evidence import EvidenceRecord
from landscape import LandscapeState
from prototype import ExecutionResult


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")


def execution_fingerprint(result: ExecutionResult) -> str:
    payload = {
        "protocol_id": result.protocol_id,
        "status": result.status,
        "transition_kind": result.transition.kind,
        "transition_data": dict(result.transition.data),
        "signals": list(result.signals),
        "steps": result.steps,
    }
    return hashlib.sha256(_canonical(payload)).hexdigest()


def evidence_fingerprint(evidence: EvidenceRecord) -> str:
    payload = {
        "protocol_id": evidence.protocol_id,
        "status": evidence.status,
        "transition_kind": evidence.transition_kind,
        "transition_data": dict(evidence.transition_data),
        "signals": list(evidence.signals),
    }
    return hashlib.sha256(_canonical(payload)).hexdigest()


def landscape_fingerprint(state: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical(dict(state))).hexdigest()


def replay_landscape(evidence_records: Iterable[EvidenceRecord]) -> Mapping[str, Any]:
    """Reconstruct a Landscape view by replaying preserved Evidence in order."""
    state = LandscapeState.empty()
    for evidence in evidence_records:
        state.apply_evidence(evidence)
    return state.snapshot()


@dataclass(frozen=True)
class ReplayResult:
    execution_fingerprint: str
    evidence_fingerprint: str
    landscape_fingerprint: str


def capture_replay(result: ExecutionResult, evidence: EvidenceRecord, landscape: Mapping[str, Any]) -> ReplayResult:
    return ReplayResult(
        execution_fingerprint=execution_fingerprint(result),
        evidence_fingerprint=evidence_fingerprint(evidence),
        landscape_fingerprint=landscape_fingerprint(landscape),
    )


def replay_matches(first: ReplayResult, second: ReplayResult) -> bool:
    return first == second

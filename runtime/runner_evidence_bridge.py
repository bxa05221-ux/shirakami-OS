"""Adapter from bounded RunnerEvidence to canonical EvidenceRecord.

The adapter preserves execution identity and observed runner state without
creating authority or interpreting execution outcomes beyond the evidence
already emitted by the Runner.
"""

from collections.abc import Iterable

try:
    from .background_runner_evidence import RunnerEvidence
    from .evidence import EvidenceRecord
except ImportError:  # legacy top-level runtime test imports
    from background_runner_evidence import RunnerEvidence
    from evidence import EvidenceRecord


def runner_evidence_to_evidence(
    evidence: RunnerEvidence,
    *,
    protocol_id: str | None = None,
) -> EvidenceRecord:
    """Convert one RunnerEvidence record into canonical immutable Evidence."""

    resolved_protocol = protocol_id or evidence.protocol_identity
    if not resolved_protocol.strip():
        raise ValueError("protocol identity is required")

    transition_data = {
        "event": evidence.event,
        "protocol_identity": evidence.protocol_identity,
        "activation_identity": evidence.activation_identity,
        "approval_identity": evidence.approval_identity,
        "run_identity": evidence.run_identity,
        "iteration": evidence.iteration,
        "runner_state": evidence.runner_state,
    }

    return EvidenceRecord(
        protocol_id=resolved_protocol,
        status="observed",
        transition_kind=f"runner:{evidence.event}",
        transition_data=transition_data,
        signals=(f"runner:{evidence.event}",),
    )


def runner_evidence_batch_to_evidence(
    evidence: Iterable[RunnerEvidence],
    *,
    protocol_id: str | None = None,
) -> tuple[EvidenceRecord, ...]:
    """Convert RunnerEvidence records without changing their order or meaning."""

    return tuple(
        runner_evidence_to_evidence(item, protocol_id=protocol_id)
        for item in evidence
    )

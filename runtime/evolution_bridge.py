"""R0100 bridge to the canonical Runtime Evidence boundary.

This module keeps the Evolution Loop state machine small while making its
records consumable by the existing immutable EvidenceRecord model.
"""

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .evidence import EvidenceRecord
from .evolution_loop import EvidenceCandidate, EvidenceClass, TransitionRecord


@dataclass(frozen=True)
class ContextSnapshot:
    """Immutable execution context captured at a loop boundary."""

    landscape: Mapping[str, Any] = field(default_factory=dict)
    protocol_id: str = ""
    runtime_state: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def as_mapping(self) -> Mapping[str, Any]:
        return {
            "landscape": dict(self.landscape),
            "protocol_id": self.protocol_id,
            "runtime_state": self.runtime_state,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class ProtocolCandidate:
    """A proposed protocol change awaiting Human Review."""

    protocol_id: str
    diff_ref: str = ""
    rationale: str = ""
    source_evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class VerificationResult:
    """Verification outcome with explicit uncertainty."""

    status: str
    uncertainty: str
    observed: Mapping[str, Any] = field(default_factory=dict)


def transition_to_evidence(
    record: TransitionRecord,
    *,
    protocol_id: str = "R0100",
) -> EvidenceRecord | None:
    """Promote a meaningful Evolution Loop transition to canonical Evidence."""

    if record.evidence_class == EvidenceClass.NONE:
        return None

    payload = dict(record.context or {})
    payload.update(
        {
            "from_state": record.from_state.value,
            "to_state": record.to_state.value,
            "event": record.event,
            "accepted": record.accepted,
            "reason": record.reason,
            "evidence_class": record.evidence_class.value,
        }
    )

    return EvidenceRecord(
        protocol_id=protocol_id,
        status="accepted" if record.accepted else "rejected",
        transition_kind=f"R0100:{record.event}",
        transition_data=payload,
        signals=(record.evidence_class.value,),
    )


def candidate_to_evidence(
    candidate: EvidenceCandidate,
    *,
    protocol_id: str = "R0100",
) -> EvidenceRecord:
    """Convert an in-memory candidate into the canonical Evidence shape."""

    payload = dict(candidate.payload)
    payload.update(
        {
            "state": candidate.state,
            "event": candidate.event,
            "evidence_class": candidate.evidence_class.value,
            "source": candidate.source,
        }
    )
    return EvidenceRecord(
        protocol_id=protocol_id,
        status="observed",
        transition_kind=f"R0100:{candidate.event}",
        transition_data=payload,
        signals=(candidate.evidence_class.value,),
    )


class EvidenceQuery:
    """Small deterministic query boundary over canonical Evidence records."""

    def __init__(self, evidence: Iterable[EvidenceRecord] = ()) -> None:
        self._evidence = tuple(evidence)

    def all(self) -> tuple[EvidenceRecord, ...]:
        return self._evidence

    def by_protocol(self, protocol_id: str) -> tuple[EvidenceRecord, ...]:
        return tuple(e for e in self._evidence if e.protocol_id == protocol_id)

    def by_signal(self, signal: str) -> tuple[EvidenceRecord, ...]:
        return tuple(e for e in self._evidence if signal in e.signals)

    def by_transition(self, transition_kind: str) -> tuple[EvidenceRecord, ...]:
        return tuple(e for e in self._evidence if e.transition_kind == transition_kind)

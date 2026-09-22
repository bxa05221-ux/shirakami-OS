"""R0100 Evidence-Driven Runtime Loop.

Small, backend-neutral state machine for the Shirakami Evolution Loop.
It validates declared transitions, records every attempted transition, and
promotes meaningful failures/mismatches/human decisions to Evidence.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class LoopState(str, Enum):
    IDLE = "IDLE"
    OBSERVE = "OBSERVE"
    EVIDENCE = "EVIDENCE"
    ANALYZE = "ANALYZE"
    PROTOCOL_CANDIDATE = "PROTOCOL_CANDIDATE"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    READY = "READY"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"
    ACCEPTED = "ACCEPTED"
    DIFF = "DIFF"
    STOPPED = "STOPPED"


class EvidenceClass(str, Enum):
    NONE = "NONE"
    OBSERVATION = "OBSERVATION"
    FAILURE = "FAILURE"
    MISMATCH = "MISMATCH"
    PROTOCOL = "PROTOCOL"
    SAFETY = "SAFETY"
    CONTEXT_SNAPSHOT = "CONTEXT_SNAPSHOT"
    HUMAN_DECISION = "HUMAN_DECISION"


@dataclass(frozen=True)
class TransitionResult:
    accepted: bool
    from_state: LoopState
    to_state: LoopState
    event: str
    reason: str = ""


@dataclass(frozen=True)
class TransitionRecord:
    from_state: LoopState
    event: str
    to_state: LoopState
    accepted: bool
    reason: str = ""
    evidence_class: EvidenceClass = EvidenceClass.NONE
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceCandidate:
    evidence_class: EvidenceClass
    source: str
    state: str
    event: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class TransitionRule:
    source: LoopState
    event: str
    target: LoopState
    evidence_class: EvidenceClass = EvidenceClass.NONE
    requires_human: bool = False


DEFAULT_RULES = (
    TransitionRule(LoopState.IDLE, "observe", LoopState.OBSERVE, EvidenceClass.OBSERVATION),
    # External Activation has already crossed the human authorization boundary.
    # This transition only synchronizes the internal execution lifecycle.
    TransitionRule(LoopState.IDLE, "activated_execution", LoopState.READY),
    TransitionRule(LoopState.OBSERVE, "evidence", LoopState.EVIDENCE),
    TransitionRule(LoopState.EVIDENCE, "analyze", LoopState.ANALYZE),
    TransitionRule(LoopState.ANALYZE, "existing_protocol", LoopState.READY),
    TransitionRule(LoopState.ANALYZE, "new_protocol", LoopState.PROTOCOL_CANDIDATE),
    TransitionRule(LoopState.PROTOCOL_CANDIDATE, "review", LoopState.HUMAN_REVIEW, EvidenceClass.PROTOCOL),
    TransitionRule(LoopState.HUMAN_REVIEW, "approve", LoopState.READY, EvidenceClass.HUMAN_DECISION, True),
    TransitionRule(LoopState.HUMAN_REVIEW, "reject", LoopState.IDLE, EvidenceClass.HUMAN_DECISION, True),
    TransitionRule(LoopState.READY, "execute", LoopState.EXECUTE),
    TransitionRule(LoopState.EXECUTE, "verify", LoopState.VERIFY),
    TransitionRule(LoopState.VERIFY, "pass", LoopState.ACCEPTED),
    TransitionRule(LoopState.VERIFY, "mismatch", LoopState.DIFF, EvidenceClass.MISMATCH),
    TransitionRule(LoopState.DIFF, "protocol_change", LoopState.PROTOCOL_CANDIDATE, EvidenceClass.MISMATCH),
    TransitionRule(LoopState.DIFF, "reobserve", LoopState.OBSERVE, EvidenceClass.MISMATCH),
    TransitionRule(LoopState.DIFF, "stop", LoopState.STOPPED, EvidenceClass.SAFETY),
    TransitionRule(LoopState.ACCEPTED, "observe", LoopState.OBSERVE, EvidenceClass.OBSERVATION),\n    TransitionRule(LoopState.ACCEPTED, "activated_execution", LoopState.READY),
    TransitionRule(LoopState.ACCEPTED, "activated_execution", LoopState.READY),
)


class EvolutionLoop:
    """Fail-closed R0100 transition runtime."""

    def __init__(self, rules=DEFAULT_RULES) -> None:
        self.state = LoopState.IDLE
        self.records: list[TransitionRecord] = []
        self.evidence: list[EvidenceCandidate] = []
        self._rules = {(r.source, r.event): r for r in rules}

    def dispatch(
        self,
        event: str,
        context: Mapping[str, Any] | None = None,
        *,
        human_approved: bool = False,
    ) -> TransitionResult:
        context = dict(context or {})
        source = self.state
        rule = self._rules.get((source, event))
        if rule is None:
            return self._record_rejection(source, event, "unknown transition", context)

        if rule.requires_human and not human_approved:
            return self._record_rejection(source, event, "human approval required", context)

        self.state = rule.target
        record = TransitionRecord(
            from_state=source,
            event=event,
            to_state=self.state,
            accepted=True,
            evidence_class=rule.evidence_class,
            context=context,
        )
        self.records.append(record)
        self._promote(record)
        return TransitionResult(True, source, self.state, event)

    def _record_rejection(
        self,
        source: LoopState,
        event: str,
        reason: str,
        context: Mapping[str, Any],
    ) -> TransitionResult:
        record = TransitionRecord(
            from_state=source,
            event=event,
            to_state=source,
            accepted=False,
            reason=reason,
            evidence_class=EvidenceClass.FAILURE,
            context=context,
        )
        self.records.append(record)
        self._promote(record)
        return TransitionResult(False, source, source, event, reason)

    def _promote(self, record: TransitionRecord) -> None:
        if record.evidence_class == EvidenceClass.NONE:
            return
        self.evidence.append(
            EvidenceCandidate(
                evidence_class=record.evidence_class,
                source="transition_record",
                state=record.to_state.value,
                event=record.event,
                payload=dict(record.context),
            )
        )

"""Minimal executable Thread RPG 3.2 runtime boundary.

Thread RPG owns interaction state and rendering. It does not infer participant
psychology or domain truth, and it keeps the AI provider behind an adapter-like
callable boundary.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence
from uuid import uuid4

from .evidence import EvidenceRecord


ANONYMOUS_GROUP_SIZE = 7


@dataclass(frozen=True)
class Turn:
    """One observable exchange in a Thread."""

    turn_id: str
    participant: str
    input: str
    response: str
    timestamp: str


@dataclass
class ThreadState:
    """Observable Thread state; no inferred psychological state is stored."""

    session_id: str
    landscape_ref: str
    status: str = "ready"
    turns: list[Turn] = field(default_factory=list)
    active_topics: list[str] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)
    temperature: str = "normal"
    tempo: str = "normal"
    evidence: list[EvidenceRecord] = field(default_factory=list)

    def snapshot(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "session_id": self.session_id,
            "landscape_ref": self.landscape_ref,
            "status": self.status,
            "turns": [turn.__dict__.copy() for turn in self.turns],
            "active_topics": list(self.active_topics),
            "unresolved_questions": list(self.unresolved_questions),
            "atmosphere": {
                "temperature": self.temperature,
                "tempo": self.tempo,
            },
        })


ResponseAdapter = Callable[[str, ThreadState], str]


@dataclass(frozen=True)
class AnonymousOpinion:
    """An AI-provided candidate opinion and its declared recommendation weight."""

    opinion_id: str
    text: str
    recommendation_weight: float


def allocate_anonymous_counts(
    opinions: Sequence[AnonymousOpinion],
    preserve_minority: bool = True,
) -> dict[str, int]:
    """Project declared recommendation weights into the fixed seven-person group."""
    if not opinions:
        return {}
    if any(op.recommendation_weight < 0 for op in opinions):
        raise ValueError("recommendation_weight must be non-negative")

    total_count = ANONYMOUS_GROUP_SIZE
    total_weight = sum(op.recommendation_weight for op in opinions)
    if total_weight <= 0:
        return {op.opinion_id: 0 for op in opinions}

    raw = [op.recommendation_weight / total_weight * total_count for op in opinions]
    counts = [int(value) for value in raw]

    if preserve_minority and total_count >= len(opinions):
        for index, op in enumerate(opinions):
            if op.recommendation_weight > 0 and counts[index] == 0:
                counts[index] = 1

    remaining = total_count - sum(counts)
    fractions = [raw[i] - int(raw[i]) for i in range(len(opinions))]

    if remaining > 0:
        order = sorted(range(len(opinions)), key=lambda i: (-fractions[i], i))
        for index in order[:remaining]:
            counts[index] += 1
    elif remaining < 0:
        order = sorted(range(len(opinions)), key=lambda i: (fractions[i], -counts[i], i))
        for index in order:
            if remaining == 0:
                break
            if counts[index] > 0:
                counts[index] -= 1
                remaining += 1

    return {op.opinion_id: count for op, count in zip(opinions, counts)}


class ThreadRuntime:
    """Small stateful runtime for the Thread RPG 3.2 implementation boundary."""

    def __init__(self, response_adapter: ResponseAdapter | None = None):
        self._sessions: dict[str, ThreadState] = {}
        self._response_adapter = response_adapter or self._default_response

    @staticmethod
    def _default_response(value: str, _state: ThreadState) -> str:
        return value

    def create_session(self, landscape_ref: str) -> ThreadState:
        if not isinstance(landscape_ref, str) or not landscape_ref.strip():
            raise ValueError("landscape_ref is required")
        session_id = str(uuid4())
        state = ThreadState(session_id=session_id, landscape_ref=landscape_ref)
        self._sessions[session_id] = state
        return state

    def get_state(self, session_id: str) -> ThreadState:
        try:
            return self._sessions[session_id]
        except KeyError as exc:
            raise KeyError(session_id) from exc

    def submit_turn(
        self,
        session_id: str,
        participant_input: str,
        participant: str = "human",
    ) -> tuple[Turn, ThreadState, EvidenceRecord]:
        if not isinstance(participant_input, str) or not participant_input.strip():
            raise ValueError("participant_input is required")

        state = self.get_state(session_id)
        state.status = "input_received"
        state.status = "observing"
        response = self._response_adapter(participant_input, state)
        state.status = "responding"

        turn = Turn(
            turn_id=str(uuid4()),
            participant=participant,
            input=participant_input,
            response=response,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        before_count = len(state.turns)
        state.turns.append(turn)
        state.status = "state_updated"

        changed = len(state.turns) != before_count
        evidence = EvidenceRecord(
            protocol_id="thread_rpg",
            status="completed",
            transition_kind="thread.turn_added",
            transition_data=MappingProxyType({
                "changed": changed,
                "session_id": session_id,
                "turn_id": turn.turn_id,
                "turn_count": len(state.turns),
            }),
            signals=("turn_added",),
            confidence="observed",
        )
        state.evidence.append(evidence)
        state.status = "waiting"
        return turn, state, evidence

    def evidence(self, session_id: str) -> list[EvidenceRecord]:
        return list(self.get_state(session_id).evidence)


class ThreadRenderer:
    """Renderer only: converts observable Thread state into human-readable data."""

    @staticmethod
    def render(state: ThreadState) -> Mapping[str, Any]:
        return {
            "session_id": state.session_id,
            "landscape_ref": state.landscape_ref,
            "status": state.status,
            "turns": [
                {
                    "participant": turn.participant,
                    "input": turn.input,
                    "response": turn.response,
                    "timestamp": turn.timestamp,
                }
                for turn in state.turns
            ],
            "atmosphere": {
                "temperature": state.temperature,
                "tempo": state.tempo,
            },
            "unresolved_questions": list(state.unresolved_questions),
        }

    @staticmethod
    def render_anonymous_group(
        opinions: Sequence[AnonymousOpinion],
        preserve_minority: bool = True,
    ) -> list[Mapping[str, Any]]:
        """Render weighted opinions as the fixed seven anonymous participants."""
        counts = allocate_anonymous_counts(opinions, preserve_minority)
        rendered: list[Mapping[str, Any]] = []
        for opinion in opinions:
            for index in range(counts[opinion.opinion_id]):
                rendered.append({
                    "participant": f"名無し-{opinion.opinion_id}-{index + 1}",
                    "opinion_id": opinion.opinion_id,
                    "text": opinion.text,
                })
        return rendered

"""Minimal executable Thread RPG 3.2 runtime boundary.

Thread RPG owns interaction state and rendering. It does not infer participant
psychology or domain truth, and it keeps the AI provider behind an adapter-like
callable boundary.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Callable, Mapping
from uuid import uuid4

from .evidence import EvidenceRecord


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
        state = ThreadState(session_id=session_id)
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

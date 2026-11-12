"""ThreadRPG v4 conversation delta landscape (not Reality state).

Five explicit generation turns are a local experimental compression cadence,
not a normative requirement of Anmon Layer v0.1 or Matome v3.2 API.
No semantic summarization or LLM invocation is performed by this module.
"""
from dataclasses import dataclass
from typing import Literal

from runtime.aats import Thread

DeltaKind = Literal["observation", "interpretation", "uncertainty", "assumption", "question", "constraint"]


@dataclass(frozen=True)
class Delta:
    kind: DeltaKind
    content: str
    source_post_indices: tuple[int, ...]
    origin: str = "unknown"
    verified: bool = False
    verification_evidence_id: str | None = None
    human_approved: bool = False


@dataclass(frozen=True)
class Layer:
    turn_from: int
    turn_to: int
    deltas: tuple[Delta, ...]
    unresolved: tuple[Delta, ...]
    raw_post_count: int


@dataclass(frozen=True)
class ConversationLandscape:
    generation_turns: int = 0
    layers: tuple[Layer, ...] = ()
    pending: tuple[Delta, ...] = ()

    def record_generation_turn(
        self, thread: Thread, deltas: tuple[Delta, ...] = ()
    ) -> "ConversationLandscape":
        """One explicit user-triggered generation cycle, including /next.

        Inputs are caller-classified candidate deltas. The raw log is not edited.
        """
        if not isinstance(thread, Thread):
            raise TypeError("thread must be a Thread")
        for delta in deltas:
            if not isinstance(delta, Delta) or not delta.content.strip():
                raise ValueError("invalid delta")
            if not delta.source_post_indices:
                raise ValueError("each delta must have a post reference")
            if any(not 0 <= i < len(thread.posts) for i in delta.source_post_indices):
                raise ValueError("delta refers to an unavailable post")
        count = self.generation_turns + 1
        pending = self.pending + deltas
        if count % 5:
            return ConversationLandscape(count, self.layers, pending)
        previous_to = self.layers[-1].turn_to if self.layers else 0
        layer = Layer(
            turn_from=previous_to + 1,
            turn_to=count,
            deltas=pending,
            unresolved=tuple(d for d in pending if d.kind in ("uncertainty", "question")),
            raw_post_count=len(thread.posts),
        )
        return ConversationLandscape(count, self.layers + (layer,), ())

    def unresolved_questions(self) -> tuple[Delta, ...]:
        """Expose open questions as candidates, never hidden user intent."""
        return tuple(
            d for layer in self.layers for d in layer.unresolved
        ) + tuple(d for d in self.pending if d.kind in ("uncertainty", "question"))

    def to_matome_draft(self) -> dict[str, list[str]]:
        """Shape-compatible draft; no claim that external Matome API ran."""
        all_deltas = tuple(d for layer in self.layers for d in layer.deltas) + self.pending
        return {
            "facts": [
                d.content for d in all_deltas
                if d.kind == "observation"
                and d.verified
                and d.human_approved
                and bool(d.verification_evidence_id)
            ],
            "interpretations": [
                d.content for d in all_deltas
                if d.kind == "interpretation"
            ],
            "unresolved": [
                d.content for d in all_deltas
                if d.kind in ("uncertainty", "question")
            ],
            "unverified": [
                d.content for d in all_deltas
                if d.kind == "observation"
                and not (
                    d.verified
                    and d.human_approved
                    and bool(d.verification_evidence_id)
                )
            ],
        }

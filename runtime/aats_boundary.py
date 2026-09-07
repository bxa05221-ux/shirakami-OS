"""AATS boundary: transient Thread simulation for human-facing expression.

AATS (ASCII Art Thread Simulator) is the original implementation lineage for
Thread RPG. This module keeps the simulation boundary generic: participants are
identified by stable IDs, while future persona/IP data remains an extension
point rather than a Kernel concern.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class Participant:
    """A transient Thread participant.

    ``persona`` is intentionally optional and opaque. Current AATS does not
    interpret or mutate it; a future IP/persona layer may attach data here.
    """

    participant_id: str
    persona: Mapping[str, object] | None = None


@dataclass(frozen=True)
class ThreadPost:
    participant_id: str
    text: str
    aa: str | None = None


@dataclass(frozen=True)
class AATSThread:
    """Observable AATS Thread state."""

    thread_id: str
    participants: tuple[Participant, ...] = field(default_factory=tuple)
    posts: tuple[ThreadPost, ...] = field(default_factory=tuple)

    def add_participant(self, participant: Participant) -> "AATSThread":
        return AATSThread(
            thread_id=self.thread_id,
            participants=self.participants + (participant,),
            posts=self.posts,
        )

    def add_post(self, post: ThreadPost) -> "AATSThread":
        return AATSThread(
            thread_id=self.thread_id,
            participants=self.participants,
            posts=self.posts + (post,),
        )

    def snapshot(self) -> dict[str, object]:
        return {
            "thread_id": self.thread_id,
            "participants": [
                {"participant_id": p.participant_id}
                for p in self.participants
            ],
            "posts": [
                {
                    "participant_id": p.participant_id,
                    "text": p.text,
                    "aa": p.aa,
                }
                for p in self.posts
            ],
        }

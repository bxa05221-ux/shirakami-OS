"""AATS (ASCII Art Thread Simulator) boundary.

AATS is the original implementation lineage of Thread RPG. It provides a
small, observable Thread space where transient participants can exchange
posts. Persona/IP data is an opaque extension point and is not interpreted by
this runtime boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class Participant:
    participant_id: str
    persona: Mapping[str, object] | None = None


@dataclass(frozen=True)
class Post:
    participant_id: str
    text: str
    aa: str | None = None


@dataclass(frozen=True)
class Thread:
    thread_id: str
    participants: tuple[Participant, ...] = field(default_factory=tuple)
    posts: tuple[Post, ...] = field(default_factory=tuple)

    def with_participant(self, participant: Participant) -> "Thread":
        return Thread(self.thread_id, self.participants + (participant,), self.posts)

    def with_post(self, post: Post) -> "Thread":
        return Thread(self.thread_id, self.participants, self.posts + (post,))

    def snapshot(self) -> dict[str, object]:
        return {
            "thread_id": self.thread_id,
            "participants": [p.participant_id for p in self.participants],
            "posts": [
                {"participant_id": p.participant_id, "text": p.text, "aa": p.aa}
                for p in self.posts
            ],
        }

"""ThreadRPG v4 turn adapter: input events and immutable thread log only.

No LLM calls, persistence, automatic execution, or Reality mutation.
Cognitive protocols remain separate and can consume exported events later.
"""
from dataclasses import dataclass
from typing import Literal

from runtime.aats import Post, Thread

TurnKind = Literal["post", "continue"]


@dataclass(frozen=True)
class TurnEvent:
    kind: TurnKind
    thread_id: str
    text: str | None = None


@dataclass(frozen=True)
class TurnResult:
    thread: Thread
    event: TurnEvent
    generate_replies: bool


def advance_turn(thread: Thread, raw_input: str | None) -> TurnResult:
    """Accept a human post or an explicit /next; never synthesize human speech.

    Whitespace-only input is equivalent to /next for clients supporting blank
    submissions. Callers must explicitly invoke this function: no auto-advance.
    """
    if raw_input is None:
        raise ValueError("missing input is not a continuation event")
    if not isinstance(raw_input, str):
        raise TypeError("input must be a string")
    value = raw_input.strip()
    if value in ("/next", ""):
        return TurnResult(thread, TurnEvent("continue", thread.thread_id), True)
    if value.startswith("/"):
        raise ValueError("unsupported command")
    return TurnResult(
        thread.with_post(Post(participant_id="icchi", text=raw_input)),
        TurnEvent("post", thread.thread_id, raw_input),
        True,
    )


def append_generated_replies(thread: Thread, replies: list[str]) -> Thread:
    """Append a bounded batch of generated anonymous posts without deciding facts."""
    if not 1 <= len(replies) <= 8:
        raise ValueError("reply batch must contain 1 to 8 posts")
    current = thread
    for reply in replies:
        if not isinstance(reply, str) or not reply.strip():
            raise ValueError("replies must be non-empty strings")
        current = current.with_post(Post(participant_id="nanashi", text=reply))
    return current

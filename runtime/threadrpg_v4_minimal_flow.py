"""Minimal, non-authoritative ThreadRPG v4 post/continue flow.

The flow uses the v4 input adapter and accepts an injected reply generator.
It neither connects an LLM nor decides facts, executes steps, mutates Reality,
or substitutes for the separate Human Gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from runtime.aats import Thread
from runtime.threadrpg_v4_renzan_kasen import SourcePost
from runtime.threadrpg_v4_turn import TurnEvent, advance_turn, append_generated_replies


@dataclass(frozen=True)
class AnonymousReply:
    """A generated utterance and explicit references to earlier raw posts.

    References are provenance only.  They do not promote an anonymous claim to
    an Icchi fact, and callers must explicitly nominate unresolved questions.
    """

    text: str
    source_post_indices: tuple[int, ...] = ()


@dataclass(frozen=True)
class ReplyProposal:
    """A variable-size reply batch; four replies are never required."""

    replies: tuple[AnonymousReply, ...]
    unresolved_post_indices: tuple[int, ...] = ()


class ReplyGenerator(Protocol):
    """Local/test or future LLM generator; the adapter performs no I/O."""

    def __call__(self, thread: Thread, event: TurnEvent) -> ReplyProposal: ...


@dataclass(frozen=True)
class MinimalFlowResult:
    """Traceable result of one explicitly requested generation cycle."""

    thread: Thread
    event: TurnEvent
    replies: tuple[AnonymousReply, ...]
    source_posts: tuple[SourcePost, ...]
    unresolved_questions: tuple[SourcePost, ...]
    human_gate_required: bool = True
    reality_mutation_permitted: bool = False
    llm_connected: bool = False


def run_minimal_flow(
    thread: Thread, raw_input: str | None, generator: ReplyGenerator
) -> MinimalFlowResult:
    """Append a human post or honour ``/next``, then append generated replies.

    Generation occurs only when this function is explicitly called.  A normal
    post is recorded verbatim by ``advance_turn``; ``/next`` adds no Icchi text.
    The generator receives that raw pre-reply log and can return 1--8 replies.
    """
    if not isinstance(thread, Thread):
        raise TypeError("thread must be a Thread")
    if not callable(generator):
        raise TypeError("generator must be callable")

    turn = advance_turn(thread, raw_input)
    proposal = generator(turn.thread, turn.event)
    if not isinstance(proposal, ReplyProposal):
        raise TypeError("generator must return ReplyProposal")
    _validate_proposal(turn.thread, proposal)

    completed = append_generated_replies(
        turn.thread, [reply.text for reply in proposal.replies]
    )
    source_posts = tuple(
        SourcePost(index, post.participant_id, post.text, post.aa)
        for index, post in enumerate(completed.posts)
    )
    unresolved = tuple(
        source_posts[index] for index in proposal.unresolved_post_indices
    )
    return MinimalFlowResult(
        thread=completed,
        event=turn.event,
        replies=proposal.replies,
        source_posts=source_posts,
        unresolved_questions=unresolved,
    )


def _validate_proposal(thread: Thread, proposal: ReplyProposal) -> None:
    if not 1 <= len(proposal.replies) <= 8:
        raise ValueError("reply batch must contain 1 to 8 replies")
    for reply in proposal.replies:
        if not isinstance(reply, AnonymousReply) or not reply.text.strip():
            raise ValueError("replies must be non-empty AnonymousReply values")
        if any(not 0 <= index < len(thread.posts) for index in reply.source_post_indices):
            raise ValueError("reply provenance must reference an earlier raw post")
    if any(not 0 <= index < len(thread.posts) for index in proposal.unresolved_post_indices):
        raise ValueError("unresolved questions must reference an earlier raw post")

"""Hanaichimonme V4: dynamic anonymous reply selection and session continuity.

This is a renderer-side selection mechanism.  It assigns neither personality
nor authority to an anonymous id, and it never changes Landscape or Reality.
Its small semantic extractor is deliberately transparent and rule based: every
link cites the exact post indices and trigger text that produced it.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from hashlib import sha256
import re
from typing import Iterable, Protocol

from runtime.aats import Thread
from runtime.threadrpg_v4_minimal_flow import AnonymousReply, ReplyGenerator, ReplyProposal, run_minimal_flow

_ANCHOR = re.compile(r">>(\d+)")
_CORRECTION = ("訂正", "違う", "いや", "修正")
_CUE = ("研究へ戻", "調べ直", "検証", "続き")


@dataclass(frozen=True)
class SemanticLink:
    relation: str
    source_post_indices: tuple[int, ...]
    trigger: str


@dataclass(frozen=True)
class SpeakerPlan:
    participant_ids: tuple[str, ...]
    links: tuple[SemanticLink, ...]
    cue_detected: bool


@dataclass(frozen=True)
class HanaichimonmeTurn:
    thread: Thread
    plan: SpeakerPlan
    replies: tuple[AnonymousReply, ...]
    semantic_history: tuple[SemanticLink, ...]
    human_gate_required: bool = True
    reality_mutation_permitted: bool = False


@dataclass
class HanaichimonmeSession:
    """Caller-owned in-memory state.  Persistence is an explicit future adapter."""

    thread: Thread
    semantic_history: list[SemanticLink] = field(default_factory=list)

    def generate(self, raw_input: str | None, generator: ReplyGenerator) -> HanaichimonmeTurn:
        preview = _preview_thread(self.thread, raw_input)
        plan = plan_speakers(preview)
        result = run_minimal_flow(
            self.thread, raw_input, _PlannedGenerator(generator, plan.participant_ids)
        )
        links = extract_semantic_links(result.thread, start=len(self.thread.posts))
        self.thread = result.thread
        self.semantic_history.extend(link for link in links if link not in self.semantic_history)
        return HanaichimonmeTurn(result.thread, plan, result.replies, tuple(self.semantic_history))


class HanaichimonmeSessionStore:
    """Process-local session holder; no cross-process durability is claimed."""

    def __init__(self) -> None:
        self._sessions: dict[str, HanaichimonmeSession] = {}

    def get(self, thread_id: str) -> HanaichimonmeSession:
        return self._sessions.setdefault(thread_id, HanaichimonmeSession(Thread(thread_id)))


class _PlannedGenerator:
    def __init__(self, generator: ReplyGenerator, participant_ids: tuple[str, ...]) -> None:
        self.generator, self.participant_ids = generator, participant_ids

    def __call__(self, thread: Thread, event: object) -> ReplyProposal:
        proposal = self.generator(thread, event)  # type: ignore[arg-type]
        if not isinstance(proposal, ReplyProposal):
            return proposal
        assigned = tuple(
            replace(reply, participant_id=reply.participant_id or self.participant_ids[index % len(self.participant_ids)])
            for index, reply in enumerate(proposal.replies)
        )
        return replace(proposal, replies=assigned)


def _preview_thread(thread: Thread, raw_input: str | None) -> Thread:
    if raw_input is None:
        return thread
    value = raw_input.strip()
    if value in ("", "/next"):
        return thread
    from runtime.aats import Post
    return thread.with_post(Post("icchi", raw_input))


def extract_semantic_links(thread: Thread, *, start: int = 0) -> tuple[SemanticLink, ...]:
    """Extract only inspectable textual relations; it does not infer wishes or facts."""
    links: list[SemanticLink] = []
    for index, post in enumerate(thread.posts[start:], start):
        for matched in _ANCHOR.finditer(post.text):
            target = int(matched.group(1)) - 1
            if 0 <= target < index:
                links.append(SemanticLink("reply", (index, target), matched.group(0)))
        for marker in _CORRECTION:
            if marker in post.text:
                links.append(SemanticLink("correction", (index,), marker))
                break
        for marker in _CUE:
            if marker in post.text:
                links.append(SemanticLink("cue", (index,), marker))
                break
    return tuple(links)


def plan_speakers(thread: Thread, *, maximum: int = 4) -> SpeakerPlan:
    """Select a variable subset from context; neither order nor participation is fixed."""
    if maximum < 1:
        raise ValueError("maximum must be positive")
    links = extract_semantic_links(thread, start=max(0, len(thread.posts) - 5))
    cue_detected = any(link.relation == "cue" for link in links)
    recent = [post.participant_id for post in thread.posts[-8:] if post.participant_id != "icchi"]
    pool = list(dict.fromkeys(reversed(recent))) + [f"nanashi-{index}" for index in range(1, 8)]
    seed = "\n".join(post.text for post in thread.posts[-5:]) + str(links)
    ranked = sorted(pool, key=lambda participant_id: sha256(f"{seed}:{participant_id}".encode()).hexdigest())
    count = 1 + (int(sha256(seed.encode()).hexdigest()[:2], 16) % maximum)
    # A cue changes the selected subset rather than restoring a fixed order.
    if cue_detected:
        count = min(maximum, count + 1)
    return SpeakerPlan(tuple(ranked[:count]), links, cue_detected)

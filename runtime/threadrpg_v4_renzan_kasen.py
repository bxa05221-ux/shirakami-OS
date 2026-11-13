"""Structured, non-authoritative connection from ThreadRPG to Renzan/Kasen.

This adapter keeps the AATS source posts intact while exposing the existing
Renzan viewpoints and Kasen re-expression. Conflicts and unanswered questions
are supplied explicitly by the caller; it performs no semantic inference and
does not execute a Small Step, mutate Reality, or contact an API.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from runtime.aats import Thread
from runtime.way import Kasen, Renzan, Viewpoint


@dataclass(frozen=True)
class SourcePost:
    """A source-addressable copy of one immutable Thread post."""

    post_index: int
    participant_id: str
    text: str
    aa: str | None


@dataclass(frozen=True)
class ExplicitConflict:
    """A caller-declared tension between two distinct source posts."""

    left: SourcePost
    right: SourcePost


@dataclass(frozen=True)
class StructuredRenzanKasenConnection:
    """Renzan/Kasen output together with its unaltered source structure."""

    source_posts: tuple[SourcePost, ...]
    viewpoints: tuple[Viewpoint, ...]
    narrative: str
    conflicts: tuple[ExplicitConflict, ...]
    unresolved_questions: tuple[SourcePost, ...]


def connect_thread(
    thread: Thread,
    *,
    conflict_pairs: Iterable[tuple[int, int]] = (),
    unresolved_post_indices: Iterable[int] = (),
) -> StructuredRenzanKasenConnection:
    """Connect one Thread to Renzan/Kasen without inferring or applying state.

    The annotations remain references to the original posts, so Kasen's prose
    cannot erase original wording, participant, AA, or unresolved questions.
    """
    if not isinstance(thread, Thread):
        raise TypeError("thread must be a Thread")

    source_posts = tuple(
        SourcePost(index, post.participant_id, post.text, post.aa)
        for index, post in enumerate(thread.posts)
    )
    viewpoints = Renzan().collect(thread)
    if len(viewpoints) != len(source_posts):
        raise ValueError("Renzan output must preserve every source post")
    for source, viewpoint in zip(source_posts, viewpoints):
        if (
            source.participant_id,
            source.text,
            source.aa,
        ) != (
            viewpoint.participant_id,
            viewpoint.text,
            viewpoint.aa,
        ):
            raise ValueError("Renzan viewpoint differs from its source post")

    conflicts = tuple(
        ExplicitConflict(
            _source_at(source_posts, left_index),
            _source_at(source_posts, right_index),
        )
        for left_index, right_index in conflict_pairs
    )
    if any(conflict.left.post_index == conflict.right.post_index for conflict in conflicts):
        raise ValueError("a conflict must reference two distinct posts")

    unresolved = tuple(
        _source_at(source_posts, post_index)
        for post_index in unresolved_post_indices
    )
    return StructuredRenzanKasenConnection(
        source_posts=source_posts,
        viewpoints=viewpoints,
        narrative=Kasen().compose(viewpoints),
        conflicts=conflicts,
        unresolved_questions=unresolved,
    )


def _source_at(source_posts: tuple[SourcePost, ...], post_index: int) -> SourcePost:
    if not isinstance(post_index, int):
        raise TypeError("post indices must be integers")
    if not 0 <= post_index < len(source_posts):
        raise IndexError("post index out of range")
    return source_posts[post_index]

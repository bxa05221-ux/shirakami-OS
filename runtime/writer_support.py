"""Minimal writer-support vertical slice.

This module keeps the one-person path explicit:
Landscape -> Renzan -> Kasen -> Human.

It does not infer hidden meaning from a scene. When the required observable
scene input is missing, it holds a question instead of fabricating content.
Authored unresolved questions are carried through unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .way import Kasen, Renzan, Viewpoint
from .aats import Participant, Post, Thread


@dataclass(frozen=True)
class WriterSupportResult:
    landscape: Mapping[str, object]
    viewpoints: tuple[Viewpoint, ...]
    reexpression: str
    unresolved_question: str | None = None
    unresolved_questions: tuple[str, ...] = ()


def support_writer(landscape: Mapping[str, object]) -> WriterSupportResult:
    """Expose observable scene material without taking over authorship.

    The accepted Landscape fields are ``observations`` and, optionally,
    ``unresolved_questions``. Both are carried without semantic interpretation.
    """
    observations = landscape.get("observations")
    if not isinstance(observations, Sequence) or isinstance(observations, (str, bytes)):
        return WriterSupportResult(
            landscape=dict(landscape),
            viewpoints=(),
            reexpression="",
            unresolved_question="この場面について、まず何が観測されているか教えてください。",
        )

    thread = Thread("writer-one-person")
    thread = thread.with_participant(Participant("author"))
    for observation in observations:
        if isinstance(observation, str) and observation:
            thread = thread.with_post(Post("author", observation))

    authored_questions = landscape.get("unresolved_questions", ())
    if not isinstance(authored_questions, Sequence) or isinstance(authored_questions, (str, bytes)):
        authored_questions = ()
    unresolved_questions = tuple(
        question for question in authored_questions if isinstance(question, str) and question
    )

    viewpoints = Renzan().collect(thread)
    return WriterSupportResult(
        landscape=dict(landscape),
        viewpoints=viewpoints,
        reexpression=Kasen().compose(viewpoints),
        unresolved_questions=unresolved_questions,
    )

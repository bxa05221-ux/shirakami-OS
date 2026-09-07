"""Minimal writer-support vertical slice.

This module keeps the one-person path explicit:
Landscape -> Renzan -> Kasen -> Human.

It does not infer hidden meaning from a scene. When the required observable
scene input is missing, it holds a question instead of fabricating content.
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


def support_writer(landscape: Mapping[str, object]) -> WriterSupportResult:
    """Expose observable scene material without taking over authorship.

    The accepted Landscape field is ``observations``: a sequence of already
    observed scene statements. They are carried into the existing Renzan /
    Kasen path without semantic interpretation.
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

    viewpoints = Renzan().collect(thread)
    return WriterSupportResult(
        landscape=dict(landscape),
        viewpoints=viewpoints,
        reexpression=Kasen().compose(viewpoints),
    )

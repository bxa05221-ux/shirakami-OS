"""Minimal Shirakami Radio rendering boundary.

Path:
Landscape -> Renzan -> Kasen -> Radio Renderer -> Human.

The renderer does not decide domain meaning. It only packages the
human-facing re-expression for radio output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .way import Kasen, Renzan, Viewpoint
from .aats import Participant, Post, Thread


@dataclass(frozen=True)
class RadioRenderResult:
    landscape: Mapping[str, object]
    viewpoints: tuple[Viewpoint, ...]
    script: str
    unresolved_questions: tuple[str, ...] = ()


def render_radio(landscape: Mapping[str, object]) -> RadioRenderResult:
    """Render observable Landscape material as a minimal radio script.

    ``observations`` and ``unresolved_questions`` are treated as authored
    fields. Missing observations are held as a question instead of being
    fabricated.
    """
    observations = landscape.get("observations")
    if not isinstance(observations, Sequence) or isinstance(observations, (str, bytes)):
        return RadioRenderResult(
            landscape=dict(landscape),
            viewpoints=(),
            script="この景色について、まず何が起きているのか教えてください。",
        )

    thread = Thread("radio-one-person")
    thread = thread.with_participant(Participant("listener"))
    for observation in observations:
        if isinstance(observation, str) and observation:
            thread = thread.with_post(Post("listener", observation))

    authored_questions = landscape.get("unresolved_questions", ())
    if not isinstance(authored_questions, Sequence) or isinstance(authored_questions, (str, bytes)):
        authored_questions = ()
    unresolved_questions = tuple(
        question for question in authored_questions if isinstance(question, str) and question
    )

    viewpoints = Renzan().collect(thread)
    body = Kasen().compose(viewpoints)
    title = landscape.get("title")
    opening = f"Shirakami Radio、{title}です。" if isinstance(title, str) and title else "Shirakami Radio、スタートです。"
    script = f"{opening} {body}".strip()

    return RadioRenderResult(
        landscape=dict(landscape),
        viewpoints=viewpoints,
        script=script,
        unresolved_questions=unresolved_questions,
    )

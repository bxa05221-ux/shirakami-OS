"""Minimal Project Landscape assembly boundary.

Assembly groups already-loaded sources without interpreting or rewriting their
meaning. Source metadata and unresolved questions remain explicit.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .project_landscape_loader import LoadedSource


@dataclass(frozen=True)
class LandscapeSource:
    source: LoadedSource


@dataclass(frozen=True)
class ProjectLandscape:
    sources: tuple[LandscapeSource, ...]
    unresolved_questions: tuple[str, ...] = ()


def assemble_landscape(
    sources: Iterable[LoadedSource],
    unresolved_questions: Iterable[str] = (),
) -> ProjectLandscape:
    """Assemble loaded sources while preserving their boundaries."""
    return ProjectLandscape(
        sources=tuple(LandscapeSource(source) for source in sources),
        unresolved_questions=tuple(unresolved_questions),
    )

"""Minimal Context Boundary implementation.

A Context Snapshot is a scoped view of a Project Landscape. It preserves
source references and unresolved questions without interpreting their meaning.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .project_landscape_assembly import LandscapeSource, ProjectLandscape


@dataclass(frozen=True)
class ContextSnapshot:
    context_id: str
    parent_landscape_ref: str
    source_refs: tuple[LandscapeSource, ...]
    unresolved_questions: tuple[str, ...]
    requested_context: str | None = None


def create_context_snapshot(
    landscape: ProjectLandscape,
    *,
    context_id: str,
    parent_landscape_ref: str,
    requested_context: str | None = None,
    source_ids: Iterable[str] | None = None,
) -> ContextSnapshot:
    """Create an explicit scoped view without rewriting landscape content."""
    selected_ids = None if source_ids is None else set(source_ids)
    sources = landscape.sources
    if selected_ids is not None:
        sources = tuple(item for item in sources if item.source.ref.id in selected_ids)

    return ContextSnapshot(
        context_id=context_id,
        parent_landscape_ref=parent_landscape_ref,
        source_refs=tuple(sources),
        unresolved_questions=landscape.unresolved_questions,
        requested_context=requested_context,
    )

"""Minimal Project Landscape Loader.

The loader selects and validates source references already declared by the
Project Source Registry. It does not interpret source meaning or rewrite
source content.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .source_registry import ACTIVE_STATUSES, SourceRef


@dataclass(frozen=True)
class LoadedSource:
    ref: SourceRef
    content: object


@dataclass(frozen=True)
class LandscapeLoadResult:
    sources: tuple[LoadedSource, ...]
    unresolved_questions: tuple[str, ...]


def load_landscape(
    refs: Iterable[SourceRef],
    source_contents: Mapping[str, object],
    *,
    include_statuses: frozenset[str] = frozenset(ACTIVE_STATUSES),
) -> LandscapeLoadResult:
    """Load declared source content in registry order.

    ``source_contents`` is an opaque mapping from source id to already
    retrieved content. Missing content becomes an unresolved question rather
    than being fabricated. Source order is preserved from the registry.
    """
    loaded: list[LoadedSource] = []
    unresolved: list[str] = []
    for ref in refs:
        if ref.status not in include_statuses:
            continue
        if ref.id not in source_contents:
            unresolved.append(f"source content unavailable: {ref.id}")
            continue
        loaded.append(LoadedSource(ref=ref, content=source_contents[ref.id]))
    return LandscapeLoadResult(tuple(loaded), tuple(unresolved))

"""Minimal boundary for human-authored context sheets.

A Context Sheet is an existing human-facing record, not a new domain model.
The runtime keeps the supplied Landscape intact and exposes only explicitly
named observations and unresolved questions for downstream processing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class ContextSheetResult:
    landscape: Mapping[str, object]
    observations: tuple[str, ...]
    unresolved_questions: tuple[str, ...]


def load_context_sheet(landscape: Mapping[str, object]) -> ContextSheetResult:
    """Load a human-authored sheet without inventing domain meaning.

    ``observations`` and ``unresolved_questions`` are optional explicit fields.
    Other fields, such as plans, assessments, dates, or identifiers, remain in
    the original Landscape and are not interpreted by this boundary.
    """
    raw_observations = landscape.get("observations", ())
    raw_questions = landscape.get("unresolved_questions", ())

    observations = _strings(raw_observations)
    unresolved_questions = _strings(raw_questions)

    return ContextSheetResult(
        landscape=dict(landscape),
        observations=observations,
        unresolved_questions=unresolved_questions,
    )


def _strings(value: object) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)

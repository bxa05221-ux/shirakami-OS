"""Minimal relation-candidate holding for the Distorted Celestial Sphere boundary.

This module stores explicitly supplied candidate relations between observed stars.
It does not form constellations, infer causality, rank candidates, or assign truth.
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RelationCandidate:
    star_ids: tuple[str, ...]
    confidence: object = None
    reversible: bool = True


class ConstellationCandidateStore:
    """Keep reversible candidate relations without synthesizing constellations."""

    def __init__(self) -> None:
        self._candidates: list[RelationCandidate] = []

    def hold(
        self,
        star_ids: Iterable[str],
        *,
        confidence: object = None,
        reversible: bool = True,
    ) -> RelationCandidate:
        ids = tuple(star_ids)
        if len(ids) < 2 or any(not isinstance(star_id, str) or not star_id.strip() for star_id in ids):
            raise ValueError("relation candidate requires at least two non-empty star ids")

        candidate = RelationCandidate(
            star_ids=ids,
            confidence=confidence,
            reversible=reversible,
        )
        self._candidates.append(candidate)
        return candidate

    def candidates(self) -> tuple[RelationCandidate, ...]:
        return tuple(self._candidates)

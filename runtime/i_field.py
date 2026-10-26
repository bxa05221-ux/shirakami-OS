"""Provisional unresolved-term boundary.

This module is intentionally domain-neutral. It treats an ``i`` term as an
unresolved item that exists only until observable information resolves it.
It does not infer meaning and does not mutate Evidence records.
"""

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class ImaginaryTerm:
    term_id: str
    side: str
    question: str
    required_evidence: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResolvedTerm:
    term_id: str
    side: str
    value: Any
    evidence_ref: str


class IField:
    """Container for unresolved terms; resolved terms leave the active i-field."""

    def __init__(self, terms: tuple[ImaginaryTerm, ...] = ()) -> None:
        self._terms: dict[str, ImaginaryTerm] = {term.term_id: term for term in terms}
        if len(self._terms) != len(terms):
            raise ValueError("term_id must be unique")
        self._resolved: list[ResolvedTerm] = []

    @property
    def unresolved(self) -> tuple[ImaginaryTerm, ...]:
        return tuple(self._terms.values())

    @property
    def resolved(self) -> tuple[ResolvedTerm, ...]:
        return tuple(self._resolved)

    def add(self, term: ImaginaryTerm) -> None:
        if term.term_id in self._terms:
            raise ValueError(f"duplicate term_id: {term.term_id}")
        self._terms[term.term_id] = term

    def can_resolve(self, term_id: str, available_evidence: Mapping[str, Any]) -> bool:
        """Return true only when every declared evidence reference is available."""
        term = self._terms.get(term_id)
        if term is None:
            raise KeyError(term_id)
        return all(ref in available_evidence for ref in term.required_evidence)

    def resolve(
        self,
        term_id: str,
        value: Any,
        evidence_ref: str,
        available_evidence: Mapping[str, Any] | None = None,
    ) -> ResolvedTerm:
        if not evidence_ref:
            raise ValueError("evidence_ref is required")
        term = self._terms.get(term_id)
        if term is None:
            raise KeyError(term_id)
        if term.required_evidence:
            if available_evidence is None:
                raise ValueError("available_evidence is required")
            if not self.can_resolve(term_id, available_evidence):
                raise ValueError("required evidence is not available")
        self._terms.pop(term_id)
        resolved = ResolvedTerm(term.term_id, term.side, value, evidence_ref)
        self._resolved.append(resolved)
        return resolved

    def unresolved_count(self) -> int:
        return len(self._terms)

    def is_resolved(self) -> bool:
        return not self._terms

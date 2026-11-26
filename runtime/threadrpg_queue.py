"""Queue-shaped, non-authoritative Thread RPG context support.

This module deliberately stores only caller-declared semantic connections.  It
does not infer a person's wishes, emotions, or priorities from prose.  Its
output is contextual material for a later response; it never chooses an action
or mutates a Landscape.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Iterable, Mapping


@dataclass(frozen=True)
class SemanticConnection:
    """A newly observed connection, declared by the caller or a reviewed tool."""

    source: str
    target: str
    relation: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> "SemanticConnection":
        return cls(
            source=str(value["source"]),
            target=str(value["target"]),
            relation=str(value["relation"]),
        )


@dataclass(frozen=True)
class ImaginaryTerm:
    """An unresolved, subject-owned wish or an explicitly hypothetical AI term."""

    term_id: str
    subject: str
    text: str
    hypothetical: bool = False
    represents_real_emotion: bool = False

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> "ImaginaryTerm":
        subject = str(value["subject"])
        hypothetical = bool(value.get("hypothetical", False))
        real_emotion = bool(value.get("represents_real_emotion", False))
        if subject == "ai" and (not hypothetical or real_emotion):
            raise ValueError("AI imaginary terms must be hypothetical and non-emotional")
        return cls(str(value["term_id"]), subject, str(value["text"]), hypothetical, real_emotion)


@dataclass(frozen=True)
class QueueItem:
    kind: str
    detail: str


@dataclass(frozen=True)
class QueueContext:
    recent_turns: tuple[str, ...]
    new_connections: tuple[SemanticConnection, ...]
    unresolved_terms: tuple[ImaginaryTerm, ...]
    queued_items: tuple[QueueItem, ...]
    growth_history: tuple[SemanticConnection, ...]
    phase_rotation: Mapping[str, object] | None


@dataclass
class ThreadRPGQueue:
    """A queue, rather than a fixed pipeline, for descriptive context only.

    `reset()` restores the default active context.  It intentionally does not
    erase growth history or resolution evidence.  There is no deletion API.
    """

    _known_connections: list[SemanticConnection] = field(default_factory=list)
    _unresolved: dict[str, ImaginaryTerm] = field(default_factory=dict)
    _resolution_evidence: dict[str, str] = field(default_factory=dict)
    _items: deque[QueueItem] = field(default_factory=deque)

    def add_terms(self, terms: Iterable[ImaginaryTerm]) -> None:
        for term in terms:
            if term.term_id not in self._resolution_evidence:
                self._unresolved[term.term_id] = term

    def resolve_term(self, term_id: str, evidence_id: str) -> None:
        if not evidence_id:
            raise ValueError("resolving an imaginary term requires evidence_id")
        if term_id not in self._unresolved:
            raise ValueError("unknown or already resolved imaginary term")
        self._resolution_evidence[term_id] = evidence_id
        del self._unresolved[term_id]
        if not self._unresolved:
            self._items.append(QueueItem("reobserve", "all currently active imaginary terms were resolved"))

    def reset(self) -> None:
        """Clear only pending work; retained history remains available."""
        self._items.clear()

    def ingest(
        self,
        recent_turns: Iterable[str],
        declared_connections: Iterable[SemanticConnection],
        *,
        phase_rotation: Mapping[str, object] | None = None,
    ) -> QueueContext:
        turns = tuple(str(turn) for turn in recent_turns)[-5:]
        known = set(self._known_connections)
        new_connections = tuple(connection for connection in declared_connections if connection not in known)
        self._known_connections.extend(new_connections)
        if new_connections:
            self._items.append(QueueItem("recursive_compare", "compare newly connected meaning with retained growth history"))
        return QueueContext(
            recent_turns=turns,
            new_connections=new_connections,
            unresolved_terms=tuple(self._unresolved.values()),
            queued_items=tuple(self._items),
            growth_history=tuple(self._known_connections),
            phase_rotation=dict(phase_rotation) if phase_rotation is not None else None,
        )

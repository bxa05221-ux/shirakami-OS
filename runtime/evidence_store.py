"""Append-only Evidence Store for R0100.

The store is deliberately small: immutable records in, deterministic queries out.
Persistence can be replaced later without changing the Evolution Loop contract.
"""

from collections.abc import Iterable
from dataclasses import dataclass

from .evidence import EvidenceRecord


@dataclass(frozen=True)
class EvidenceStore:
    _records: tuple[EvidenceRecord, ...] = ()

    def append(self, record: EvidenceRecord) -> "EvidenceStore":
        if not isinstance(record, EvidenceRecord):
            raise TypeError("EvidenceStore accepts EvidenceRecord only")
        return EvidenceStore(self._records + (record,))

    def extend(self, records: Iterable[EvidenceRecord]) -> "EvidenceStore":
        store = self
        for record in records:
            store = store.append(record)
        return store

    def all(self) -> tuple[EvidenceRecord, ...]:
        return self._records

    def by_protocol(self, protocol_id: str) -> tuple[EvidenceRecord, ...]:
        return tuple(r for r in self._records if r.protocol_id == protocol_id)

    def by_signal(self, signal: str) -> tuple[EvidenceRecord, ...]:
        return tuple(r for r in self._records if signal in r.signals)

    def by_transition(self, transition_kind: str) -> tuple[EvidenceRecord, ...]:
        return tuple(r for r in self._records if r.transition_kind == transition_kind)

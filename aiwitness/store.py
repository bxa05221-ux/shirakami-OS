"""Append-only storage for AIwitness observations."""

from __future__ import annotations

from .witness import WitnessRecord


class WitnessStore:
    """In-memory append-only witness record store."""

    def __init__(self) -> None:
        self._records: dict[str, list[WitnessRecord]] = {}

    def record(self, witness: WitnessRecord) -> WitnessRecord:
        self._records.setdefault(witness.trace_id, []).append(witness)
        return witness

    def get(self, trace_id: str) -> WitnessRecord | None:
        records = self._records.get(trace_id)
        return records[-1] if records else None

    def get_by_witness_id(self, witness_id: str) -> WitnessRecord | None:
        for witness in self.all():
            if witness.witness_id == witness_id:
                return witness
        return None

    def history(self, trace_id: str) -> tuple[WitnessRecord, ...]:
        return tuple(self._records.get(trace_id, ()))

    def all(self) -> tuple[WitnessRecord, ...]:
        return tuple(
            witness
            for records in self._records.values()
            for witness in records
        )

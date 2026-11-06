"""Tamper-evident local audit chain prototype.

Not durable, independently witnessed, or tamper-proof. Synthetic data only.
The chain detects edits if its trusted final digest is preserved separately.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json

@dataclass(frozen=True)
class ChainedAuditEntry:
    sequence: int
    project_id: str
    record_id: str
    actor_id: str
    action: str
    occurred_at: str
    previous_digest: str
    digest: str

class LocalAuditChain:
    GENESIS = "0" * 64

    def __init__(self) -> None:
        self._entries: list[ChainedAuditEntry] = []

    @staticmethod
    def _digest(sequence: int, project_id: str, record_id: str, actor_id: str, action: str, occurred_at: str, previous_digest: str) -> str:
        canonical = json.dumps(
            [sequence, project_id, record_id, actor_id, action, occurred_at, previous_digest],
            ensure_ascii=False, separators=(",", ":"),
        ).encode("utf-8")
        return sha256(canonical).hexdigest()

    def append(self, project_id: str, record_id: str, actor_id: str, action: str, occurred_at: str | None = None) -> ChainedAuditEntry:
        from datetime import datetime, timezone
        if occurred_at is None:
            occurred_at = datetime.now(timezone.utc).isoformat()
        previous = self._entries[-1].digest if self._entries else self.GENESIS
        sequence = len(self._entries) + 1
        digest = self._digest(sequence, project_id, record_id, actor_id, action, occurred_at, previous)
        entry = ChainedAuditEntry(sequence, project_id, record_id, actor_id, action, occurred_at, previous, digest)
        self._entries.append(entry)
        return entry

    def snapshot(self) -> tuple[ChainedAuditEntry, ...]:
        return tuple(self._entries)

    @classmethod
    def verify(cls, entries: tuple[ChainedAuditEntry, ...], expected_head: str | None = None) -> bool:
        previous = cls.GENESIS
        for sequence, entry in enumerate(entries, start=1):
            if entry.sequence != sequence or entry.previous_digest != previous:
                return False
            if entry.digest != cls._digest(
                entry.sequence, entry.project_id, entry.record_id,
                entry.actor_id, entry.action, entry.occurred_at, entry.previous_digest,
            ):
                return False
            previous = entry.digest
        return expected_head is None or previous == expected_head

    @property
    def head_digest(self) -> str:
        return self._entries[-1].digest if self._entries else self.GENESIS

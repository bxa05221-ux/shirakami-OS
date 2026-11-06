"""Atomic SQLite persistence prototype for encrypted evaluation records and audit chain.

Synthetic data only. Does not manage encryption keys, IAM, or external head custody.
SQLite is local-only; callers must never store plaintext in ciphertext.
"""
from __future__ import annotations

import sqlite3
from hashlib import sha256
from pathlib import Path

from security.audit_chain import LocalAuditChain


class PersistenceIntegrityError(RuntimeError):
    pass


class AtomicEvaluationJournal:
    def __init__(self, path: str | Path):
        self.path = str(path)
        with self._connect() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("""CREATE TABLE IF NOT EXISTS records (
                record_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                ciphertext BLOB NOT NULL,
                key_version TEXT NOT NULL
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS audit (
                sequence INTEGER PRIMARY KEY,
                project_id TEXT NOT NULL,
                record_id TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                action TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                previous_digest TEXT NOT NULL,
                digest TEXT NOT NULL
            )""")

    def _connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.execute("PRAGMA busy_timeout=5000")
        return db

    def append_encrypted_record(
        self, *, record_id: str, project_id: str, owner_id: str,
        ciphertext: bytes, key_version: str, occurred_at: str,
    ) -> str:
        if not all((record_id, project_id, owner_id, ciphertext, key_version, occurred_at)):
            raise ValueError("complete encrypted record and audit metadata required")
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            rows = db.execute(
                "SELECT sequence, project_id, record_id, actor_id, action, occurred_at, previous_digest, digest FROM audit ORDER BY sequence"
            ).fetchall()
            chain = LocalAuditChain()
            for seq, project, record, actor, action, timestamp, previous, digest in rows:
                entry = chain.append(project, record, actor, action, timestamp)
                if (entry.sequence, entry.previous_digest, entry.digest) != (seq, previous, digest):
                    raise PersistenceIntegrityError("stored audit chain is invalid")
            db.execute(
                "INSERT INTO records(record_id,project_id,owner_id,ciphertext,key_version) VALUES (?,?,?,?,?)",
                (record_id, project_id, owner_id, ciphertext, key_version),
            )
            entry = chain.append(project_id, record_id, owner_id, "write:" + key_version + ":" + sha256(ciphertext).hexdigest(), occurred_at)
            db.execute(
                "INSERT INTO audit VALUES (?,?,?,?,?,?,?,?)",
                (entry.sequence, entry.project_id, entry.record_id, entry.actor_id,
                 entry.action, entry.occurred_at, entry.previous_digest, entry.digest),
            )
            return entry.digest

    def load_encrypted_record(self, record_id: str, project_id: str, *, expected_head: str | None = None) -> tuple[bytes, str] | None:
        if expected_head is None:
            raise PersistenceIntegrityError("trusted external audit head is required for reads")
        if not self.verify(expected_head=expected_head):
            raise PersistenceIntegrityError("stored journal integrity verification failed")
        with self._connect() as db:
            row = db.execute(
                "SELECT ciphertext,key_version FROM records WHERE record_id=? AND project_id=?",
                (record_id, project_id),
            ).fetchone()
            return (bytes(row[0]), row[1]) if row else None

    def verify(self, expected_head: str | None = None) -> bool:
        with self._connect() as db:
            rows = db.execute(
                "SELECT sequence,project_id,record_id,actor_id,action,occurred_at,previous_digest,digest FROM audit ORDER BY sequence"
            ).fetchall()
            chain = LocalAuditChain()
            for seq, project, record, actor, action, timestamp, previous, digest in rows:
                entry = chain.append(project, record, actor, action, timestamp)
                if (entry.sequence, entry.previous_digest, entry.digest) != (seq, previous, digest):
                    return False
            if expected_head is not None and chain.head_digest != expected_head:
                return False
            # Every stored record must be backed by a matching, chained write event.
            records = db.execute("SELECT record_id,project_id,owner_id,ciphertext,key_version FROM records").fetchall()
            expected_writes = {(rid, project, owner, "write:" + version + ":" + sha256(bytes(cipher)).hexdigest())
                               for rid, project, owner, cipher, version in records}
            chained_writes = {(record, project, actor, action)
                              for _, project, record, actor, action, _, _, _ in rows
                              if action.startswith("write:")}
            return expected_writes == chained_writes

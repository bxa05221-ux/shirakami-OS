"""Encrypted local records with project/evaluator access separation.

This is an in-process reference implementation. Production requires durable
encrypted media and managed key custody before real data is accepted.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from cryptography.fernet import Fernet, InvalidToken

class AccessDenied(PermissionError): pass
class EncryptionError(ValueError): pass

@dataclass(frozen=True)
class AccessAuditEvent:
    project_id: str; record_id: str; actor_id: str; action: str; occurred_at: str
@dataclass(frozen=True)
class _Record:
    project_id: str; owner_id: str; readers: frozenset[str]; ciphertext: bytes; key_version: str

class RotatingKeyring:
    def __init__(self, keys: dict[str, bytes], active_version: str) -> None:
        if active_version not in keys: raise EncryptionError("active key version is unavailable")
        try: self._keys = {version: Fernet(key) for version, key in keys.items()}
        except (TypeError, ValueError) as exc: raise EncryptionError("invalid encryption key") from exc
        self.active_version = active_version
    def encrypt(self, plaintext: bytes) -> tuple[str, bytes]:
        return self.active_version, self._keys[self.active_version].encrypt(plaintext)
    def decrypt(self, version: str, ciphertext: bytes) -> bytes:
        try: return self._keys[version].decrypt(ciphertext)
        except (KeyError, InvalidToken) as exc: raise EncryptionError("encrypted record cannot be decrypted") from exc

class EncryptedEvaluationStore:
    def __init__(self, keyring: RotatingKeyring) -> None:
        self._keyring, self._records, self._audit = keyring, {}, []
        self._memberships: dict[str, set[str]] = {}
    def register_project_members(self, project_id: str, evaluator_ids: set[str]) -> None:
        """Bootstrap only: caller must be a trusted local administrator, never an HTTP user."""
        if not project_id or not evaluator_ids or any(not item for item in evaluator_ids):
            raise ValueError("valid project membership is required")
        self._memberships[project_id] = set(evaluator_ids)
    def _require_member(self, project_id: str, evaluator_id: str) -> None:
        if evaluator_id not in self._memberships.get(project_id, set()):
            raise AccessDenied("evaluator is not a registered member of this project")
    def put_private(self, record_id: str, project_id: str, evaluator_id: str, content: bytes) -> None:
        self._require_member(project_id, evaluator_id)
        if record_id in self._records:
            raise AccessDenied("record id already exists")
        version, ciphertext = self._keyring.encrypt(content)
        self._records[record_id] = _Record(project_id, evaluator_id, frozenset({evaluator_id}), ciphertext, version)
        self._record(project_id, record_id, evaluator_id, "write")
    def share_for_consensus(self, record_id: str, actor_id: str, recipients: set[str]) -> None:
        record = self._require_owner(record_id, actor_id)
        self._require_member(record.project_id, actor_id)
        if not recipients or any(member not in self._memberships.get(record.project_id, set()) for member in recipients):
            raise AccessDenied("consensus recipients must belong to the same project")
        self._records[record_id] = _Record(record.project_id, record.owner_id, frozenset({record.owner_id, *recipients}), record.ciphertext, record.key_version)
        self._record(record.project_id, record_id, actor_id, "share_for_consensus")
    def revoke_consensus(self, record_id: str, actor_id: str) -> None:
        record = self._require_owner(record_id, actor_id)
        self._require_member(record.project_id, actor_id)
        self._records[record_id] = _Record(record.project_id, record.owner_id, frozenset({record.owner_id}), record.ciphertext, record.key_version)
        self._record(record.project_id, record_id, actor_id, "revoke_consensus")
    def read(self, record_id: str, project_id: str, actor_id: str) -> bytes:
        record = self._records.get(record_id)
        if record is None or record.project_id != project_id or actor_id not in record.readers or actor_id not in self._memberships.get(project_id, set()):
            self._record(project_id, record_id, actor_id, "denied")
            raise AccessDenied("record is not shared with this evaluator in this project")
        self._record(project_id, record_id, actor_id, "read")
        return self._keyring.decrypt(record.key_version, record.ciphertext)
    def audit_events(self) -> tuple[AccessAuditEvent, ...]: return tuple(self._audit)
    def _require_owner(self, record_id: str, actor_id: str) -> _Record:
        record = self._records.get(record_id)
        if record is None or record.owner_id != actor_id: raise AccessDenied("only the owner can share a private record")
        return record
    def _record(self, project_id: str, record_id: str, actor_id: str, action: str) -> None:
        self._audit.append(AccessAuditEvent(project_id, record_id, actor_id, action, datetime.now(timezone.utc).isoformat()))

"""Fail-closed policy enforcement for every external model handoff.

Provider adapters must obtain an immutable authorization here before they can
serialize a request for an external provider.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping
from uuid import uuid4

class PolicyDenied(RuntimeError):
    """Raised when an external transmission is not explicitly allowed."""

def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

@dataclass(frozen=True)
class OutboundPolicy:
    policy_id: str
    version: str
    enabled: bool
    allowed_destinations: frozenset[tuple[str, str]]
    allowed_data_classes: frozenset[str]

@dataclass(frozen=True)
class AuthorizedHandoff:
    authorization_id: str
    policy_id: str
    policy_version: str
    provider: str
    model: str
    data_classification: str
    payload: Any
    payload_fingerprint: str

@dataclass(frozen=True)
class PolicyAuditEvent:
    authorization_id: str | None
    outcome: str
    reason: str
    provider: str
    model: str
    data_classification: str | None
    payload_fingerprint: str | None

class PolicyAuditStore:
    """Append-only metadata-only audit sink; request content is never retained."""
    def __init__(self) -> None:
        self._events: list[PolicyAuditEvent] = []
    def append(self, event: PolicyAuditEvent) -> None:
        self._events.append(event)
    def all(self) -> tuple[PolicyAuditEvent, ...]:
        return tuple(self._events)

class AIwitnessPolicyGate:
    """Default-deny outbound gate for one configured provider/model pair."""
    def __init__(self, policy: OutboundPolicy | None, audit: PolicyAuditStore | None = None) -> None:
        self._policy = policy
        self._audit = audit or PolicyAuditStore()
    @property
    def audit(self) -> PolicyAuditStore:
        return self._audit
    def authorize(self, handoff: Mapping[str, Any], *, provider: str, model: str) -> AuthorizedHandoff:
        payload = handoff.get("input", handoff.get("payload"))
        classification = handoff.get("data_classification")
        fingerprint = sha256(_canonical(payload)).hexdigest() if payload is not None else None
        try:
            if self._policy is None or not self._policy.enabled:
                raise PolicyDenied("outbound policy is unavailable or disabled")
            if not isinstance(classification, str) or not classification:
                raise PolicyDenied("data classification is required")
            if classification in {"personal_information", "raw_evaluation_record", "confidential_context", "unknown"}:
                raise PolicyDenied("restricted data class cannot leave the local boundary")
            if (provider, model) not in self._policy.allowed_destinations:
                raise PolicyDenied("destination is not explicitly allowed")
            if classification not in self._policy.allowed_data_classes:
                raise PolicyDenied("data class is not explicitly allowed")
            if payload is None:
                raise PolicyDenied("classified payload is required")
            authorized = AuthorizedHandoff(str(uuid4()), self._policy.policy_id, self._policy.version, provider, model, classification, json.loads(_canonical(payload)), fingerprint or "")
        except PolicyDenied as exc:
            self._audit.append(PolicyAuditEvent(None, "denied", str(exc), provider, model, classification if isinstance(classification, str) else None, fingerprint))
            raise
        self._audit.append(PolicyAuditEvent(authorized.authorization_id, "allowed", "explicit policy match", provider, model, classification, authorized.payload_fingerprint))
        return authorized
    def verify(self, authorized: AuthorizedHandoff, *, provider: str, model: str) -> None:
        if self._policy is None or not self._policy.enabled:
            raise PolicyDenied("outbound policy is unavailable or disabled")
        if authorized.provider != provider or authorized.model != model:
            raise PolicyDenied("authorized destination was changed")
        if authorized.policy_id != self._policy.policy_id or authorized.policy_version != self._policy.version:
            raise PolicyDenied("authorization does not match active policy")
        if sha256(_canonical(authorized.payload)).hexdigest() != authorized.payload_fingerprint:
            raise PolicyDenied("authorized payload was changed")

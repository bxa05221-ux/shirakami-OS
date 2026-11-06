"""Trusted, in-process evaluator identity registry (reference implementation only).

Credentials and project grants must be provisioned by a trusted administrator,
never through evaluator-controlled HTTP requests. This is not production IAM.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest

class EvaluatorAuthDenied(PermissionError):
    pass

@dataclass(frozen=True)
class EvaluatorPrincipal:
    evaluator_id: str
    project_ids: frozenset[str]

class EvaluatorIdentityRegistry:
    def __init__(self) -> None:
        self._tokens: dict[str, EvaluatorPrincipal] = {}

    def provision(self, token: str, evaluator_id: str, project_ids: set[str]) -> None:
        if not token or len(token) < 32 or not evaluator_id or not project_ids or any(not p for p in project_ids):
            raise ValueError("trusted provisioning requires a strong token, identity and project grants")
        fingerprint = sha256(token.encode("utf-8")).hexdigest()
        if fingerprint in self._tokens:
            raise ValueError("credential is already provisioned")
        self._tokens[fingerprint] = EvaluatorPrincipal(evaluator_id, frozenset(project_ids))

    def authenticate(self, token: str | None, project_id: str) -> EvaluatorPrincipal:
        if not token or not project_id:
            raise EvaluatorAuthDenied("credential and project are required")
        fingerprint = sha256(token.encode("utf-8")).hexdigest()
        # Compare against provisioned fingerprints without exposing token material.
        principal = None
        for stored, candidate in self._tokens.items():
            if compare_digest(stored, fingerprint):
                principal = candidate
        if principal is None or project_id not in principal.project_ids:
            raise EvaluatorAuthDenied("evaluator is not authorized for this project")
        return principal

    def revoke(self, token: str) -> None:
        self._tokens.pop(sha256(token.encode("utf-8")).hexdigest(), None)

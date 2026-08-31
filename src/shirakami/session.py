"""Minimal in-memory session context for the OPPAI-Shirakami runtime."""

from typing import Any


class SessionStore:
    def __init__(self) -> None:
        self._contexts: dict[str, dict[str, Any]] = {}

    def get(self, session_id: str) -> dict[str, Any]:
        return dict(self._contexts.get(session_id, {}))

    def update(self, session_id: str, context_delta: dict[str, Any]) -> dict[str, Any]:
        current = self._contexts.setdefault(session_id, {})
        current.update(context_delta)
        return dict(current)

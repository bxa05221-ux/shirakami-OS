"""GitHub Landscape Adapter boundary for Shirakami Runtime β0.1.

This module intentionally contains only the adapter contract and data mapping.
Actual GitHub transport is kept behind a small injected client so Runtime core
remains independent of GitHub.
"""

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from evidence import EvidenceRecord, is_transition_evidence


class GitHubClient(Protocol):
    def read_landscape(self) -> Mapping[str, Any]: ...

    def write_landscape(self, transition: Mapping[str, Any]) -> None: ...


@dataclass
class GitHubLandscapeAdapter:
    """Concrete Landscape Adapter backed by an injected GitHub client."""

    client: GitHubClient

    def read_state(self) -> Mapping[str, Any]:
        return dict(self.client.read_landscape())

    def apply_transition(self, evidence: EvidenceRecord) -> None:
        if not is_transition_evidence(evidence):
            return

        self.client.write_landscape(dict(evidence.transition_data))


class FakeGitHubClient:
    """Deterministic test double for the GitHub boundary."""

    def __init__(self, initial_state: Mapping[str, Any] | None = None) -> None:
        self._state = dict(initial_state or {})

    def read_landscape(self) -> Mapping[str, Any]:
        return dict(self._state)

    def write_landscape(self, transition: Mapping[str, Any]) -> None:
        self._state.update(dict(transition))

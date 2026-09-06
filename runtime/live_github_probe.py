"""Operational probe for a read-only Runtime -> GitHub Landscape path.

The credential is supplied by an external provider and is never persisted here.
This module deliberately performs no write and makes no semantic interpretation.
"""

from __future__ import annotations

from typing import Callable, Mapping

from .github_client import GitHubContentsClient
from .github_repository_landscape import GitHubRepositoryLandscapeAdapter


def read_live_repository_landscape(
    owner: str,
    repo: str,
    token_provider: Callable[[], str],
    *,
    branch: str = "main",
) -> Mapping[str, object]:
    """Read the repository root through the Runtime adapter boundary."""
    client = GitHubContentsClient(
        owner=owner,
        repo=repo,
        landscape_path="",
        token_provider=token_provider,
        branch=branch,
    )
    adapter = GitHubRepositoryLandscapeAdapter(client)
    return adapter.read_state()

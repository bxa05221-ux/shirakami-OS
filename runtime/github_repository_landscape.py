"""Read-only GitHub repository Landscape adapter for β0.1 observation."""

from typing import Any, Mapping, Protocol


class RepositoryLandscapeClient(Protocol):
    def read_repository_root(self) -> Mapping[str, Any]: ...


class GitHubRepositoryLandscapeAdapter:
    """Expose observed repository structure without inventing a schema or write path."""

    def __init__(self, client: RepositoryLandscapeClient) -> None:
        self._client = client

    def read_state(self) -> Mapping[str, Any]:
        return self._client.read_repository_root()

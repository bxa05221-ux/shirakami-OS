from dataclasses import dataclass


@dataclass(frozen=True)
class GitHubProtocolSource:
    repository: str
    path: str
    ref: str | None
    content: str


class GitHubAdapter:
    """Minimal transport boundary for Protocol artifacts stored on GitHub."""

    def load_source(self, repository: str, path: str, content: str, ref: str | None = None) -> GitHubProtocolSource:
        return GitHubProtocolSource(
            repository=repository,
            path=path,
            ref=ref,
            content=content,
        )

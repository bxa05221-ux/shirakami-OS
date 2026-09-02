"""GitHub-backed Protocol Loader boundary.

Fetches a protocol document through the GitHub Contents adapter and delegates
parsing to the existing local Protocol Loader. The adapter owns retrieval;
the protocol loader owns interpretation.
"""

from __future__ import annotations

from .github_client import GitHubContentsClient
from .protocol_loader import ProtocolIR, parse_matome


class GitHubProtocolLoader:
    """Load a Matome YAML protocol from GitHub into the existing ProtocolIR."""

    def __init__(self, client: GitHubContentsClient) -> None:
        self.client = client

    def load(self, path: str) -> ProtocolIR:
        """Fetch ``path`` from GitHub and parse it with the existing loader."""
        payload = self.client.get(path)
        if isinstance(payload, dict) and "content" in payload:
            content = payload["content"]
        elif isinstance(payload, str):
            content = payload
        else:
            raise TypeError("GitHub protocol payload must contain text content")
        return parse_matome(content)

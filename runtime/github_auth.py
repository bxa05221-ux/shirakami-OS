"""Authentication boundary for GitHub transport.

Credentials are supplied by the execution environment and are never stored in
Runtime source, Landscape state, Evidence, or repository files.
"""

import os
from typing import Protocol


class TokenProvider(Protocol):
    def get_token(self) -> str: ...


class EnvironmentTokenProvider:
    """Read a GitHub token from an environment variable at call time."""

    def __init__(self, variable: str = "GITHUB_TOKEN") -> None:
        self.variable = variable

    def get_token(self) -> str:
        token = os.environ.get(self.variable)
        if not token:
            raise RuntimeError(f"GitHub token is unavailable: {self.variable}")
        return token


def authorization_header(provider: TokenProvider) -> dict[str, str]:
    return {"Authorization": f"Bearer {provider.get_token()}"}

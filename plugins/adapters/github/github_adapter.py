"""Minimal GitHub Backend adapter for controlled read/write operations.

The adapter contains GitHub-specific transport details. Runtime code should
use this boundary rather than importing GitHub APIs directly.
"""

from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class GitHubFile:
    repository: str
    path: str
    sha: str
    content: str


class GitHubAdapter:
    def __init__(self, token: str | None = None, api_base: str = "https://api.github.com"):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.api_base = api_base.rstrip("/")

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        data = json.dumps(body).encode() if body is not None else None
        request = Request(f"{self.api_base}{path}", data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=15) as response:
                return json.loads(response.read().decode())
        except HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc

    def read_file(self, repository: str, path: str, ref: str = "main") -> GitHubFile:
        result = self._request("GET", f"/repos/{repository}/contents/{path}?ref={ref}")
        if result.get("type") != "file":
            raise ValueError("GitHub path is not a file")
        content = base64.b64decode(result["content"]).decode("utf-8")
        return GitHubFile(repository, path, result["sha"], content)

    def write_file(
        self,
        repository: str,
        path: str,
        content: str,
        message: str,
        sha: str,
        branch: str = "main",
    ) -> GitHubFile:
        if not self.token:
            raise PermissionError("GITHUB_TOKEN is required for controlled write")
        result = self._request(
            "PUT",
            f"/repos/{repository}/contents/{path}",
            {
                "message": message,
                "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
                "sha": sha,
                "branch": branch,
            },
        )
        return self.read_file(repository, path, branch)

"""Minimal GitHub Contents API client for the Landscape Adapter."""

import base64
import json
from dataclasses import dataclass
from typing import Any, Callable, Mapping
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class GitHubTransportError(RuntimeError):
    pass


@dataclass
class GitHubContentsClient:
    owner: str
    repo: str
    landscape_path: str
    token_provider: Callable[[], str]
    api_base: str = "https://api.github.com"
    branch: str = "main"

    def _request(self, method: str, url: str, body: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
        token = self.token_provider()
        if not token:
            raise GitHubTransportError("GitHub token is not configured")
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        data = json.dumps(body).encode("utf-8") if body is not None else None
        if data is not None:
            headers["Content-Type"] = "application/json"
        request = Request(url, data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise GitHubTransportError(f"GitHub API request failed: {exc.code} {detail}") from exc

    def read_landscape(self) -> Mapping[str, Any]:
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/{self.landscape_path}?ref={self.branch}"
        payload = self._request("GET", url)
        if payload.get("encoding") != "base64":
            raise GitHubTransportError("Landscape file is not returned as base64 content")
        raw = base64.b64decode(payload["content"].replace("\n", "")).decode("utf-8")
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise GitHubTransportError("Landscape JSON root must be an object")
        return value

    def write_landscape(self, transition: Mapping[str, Any]) -> None:
        current_url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/{self.landscape_path}?ref={self.branch}"
        current = self._request("GET", current_url)
        current_sha = current.get("sha")
        if not current_sha:
            raise GitHubTransportError("GitHub did not return the current landscape file SHA")
        current_state = self.read_landscape()
        current_state.update(dict(transition))
        encoded = base64.b64encode(
            json.dumps(current_state, ensure_ascii=False, indent=2).encode("utf-8")
        ).decode("ascii")
        write_url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/{self.landscape_path}"
        self._request("PUT", write_url, {
            "message": "runtime: apply landscape transition",
            "content": encoded,
            "sha": current_sha,
            "branch": self.branch,
        })

    def read_repository_root(self) -> Mapping[str, Any]:
        """Read the observable root structure without defining a repository schema."""
        url = f"{self.api_base}/repos/{self.owner}/{self.repo}/contents/?ref={self.branch}"
        payload = self._request("GET", url)
        if not isinstance(payload, list):
            raise GitHubTransportError("GitHub repository root is not a directory listing")
        entries = [
            {"name": item.get("name"), "path": item.get("path"), "type": item.get("type")}
            for item in payload
        ]
        return {"repository": f"{self.owner}/{self.repo}", "branch": self.branch, "entries": entries}

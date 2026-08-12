import base64
import json

import pytest

from plugins.adapters.github.github_adapter import GitHubAdapter


class FakeAdapter(GitHubAdapter):
    def __init__(self):
        super().__init__(token="test-token", api_base="https://example.invalid")
        self.calls = []
        self.state = {"sha": "old-sha", "content": "before"}

    def _request(self, method, path, body=None):
        self.calls.append((method, path, body))
        if method == "GET":
            return {
                "type": "file",
                "sha": self.state["sha"],
                "content": base64.b64encode(self.state["content"].encode()).decode(),
            }
        self.state = {"sha": "new-sha", "content": base64.b64decode(body["content"]).decode()}
        return {"content": {"sha": "new-sha"}}


def test_controlled_write_is_followed_by_read_back():
    adapter = FakeAdapter()

    before = adapter.read_file("owner/repo", "landscape.md")
    after = adapter.write_file(
        "owner/repo",
        "landscape.md",
        "after",
        "controlled transition",
        before.sha,
    )

    assert before.content == "before"
    assert after.content == "after"
    assert after.sha == "new-sha"
    assert [call[0] for call in adapter.calls] == ["GET", "PUT", "GET"]


def test_write_requires_token():
    adapter = GitHubAdapter(token=None)
    adapter._request = lambda *args, **kwargs: pytest.fail("request must not be made")

    with pytest.raises(PermissionError, match="GITHUB_TOKEN"):
        adapter.write_file("owner/repo", "x.md", "x", "test", "sha")

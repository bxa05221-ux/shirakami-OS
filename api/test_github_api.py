from api.runtime_api import github_controlled_write, github_read
from plugins.adapters.github.github_adapter import GitHubFile


class FakeGitHubAdapter:
    def __init__(self):
        self.file = GitHubFile("owner/repo", "landscape.md", "sha-1", "before")

    def read_file(self, repository, path, ref="main"):
        assert repository == self.file.repository
        assert path == self.file.path
        return self.file

    def write_file(self, repository, path, content, message, sha, branch="main"):
        assert sha == "sha-1"
        self.file = GitHubFile(repository, path, "sha-2", content)
        return self.file


def test_api_github_read_crosses_adapter_boundary():
    result = github_read(
        {"repository": "owner/repo", "path": "landscape.md"},
        FakeGitHubAdapter(),
    )
    assert result["event"] == "backend.observed"
    assert result["content"] == "before"


def test_api_github_write_returns_read_back_evidence():
    adapter = FakeGitHubAdapter()
    result = github_controlled_write(
        {
            "repository": "owner/repo",
            "path": "landscape.md",
            "content": "after",
            "message": "controlled transition",
            "sha": "sha-1",
        },
        adapter,
    )
    assert result["event"] == "backend.write.readback"
    assert result["content"] == "after"
    assert result["evidence"]["read_back"] is True

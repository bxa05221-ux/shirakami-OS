from dataclasses import dataclass

from api.runtime_api import github_read


@dataclass(frozen=True)
class StubFile:
    repository: str
    path: str
    sha: str
    content: str


class StubGitHubAdapter:
    def read_file(self, repository: str, path: str, ref: str = "main") -> StubFile:
        assert repository == "bxa05221-ux/shirakami-OS"
        assert path == "README.md"
        assert ref == "main"
        return StubFile(repository, path, "stub-read-sha", "# observed")


def test_r0063_github_read_preserves_adapter_boundary():
    result = github_read(
        {
            "repository": "bxa05221-ux/shirakami-OS",
            "path": "README.md",
            "ref": "main",
        },
        adapter=StubGitHubAdapter(),
    )

    assert result == {
        "repository": "bxa05221-ux/shirakami-OS",
        "path": "README.md",
        "sha": "stub-read-sha",
        "content": "# observed",
        "event": "backend.observed",
    }

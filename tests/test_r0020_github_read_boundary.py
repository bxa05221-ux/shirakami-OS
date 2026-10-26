from runtime.github_client import GitHubContentsClient
from runtime.github_repository_landscape import GitHubRepositoryLandscapeAdapter


class FakeClient:
    def __init__(self):
        self.calls = 0

    def read_repository_root(self):
        self.calls += 1
        return {
            "repository": "example/repository",
            "branch": "main",
            "entries": [{"name": "README.md", "path": "README.md", "type": "file"}],
        }


def test_repository_landscape_adapter_is_read_only_representation():
    client = FakeClient()
    adapter = GitHubRepositoryLandscapeAdapter(client)

    observed = adapter.read_state()

    assert observed["repository"] == "example/repository"
    assert observed["branch"] == "main"
    assert observed["entries"][0]["path"] == "README.md"
    assert client.calls == 1
    assert set(observed) == {"repository", "branch", "entries"}


def test_github_contents_client_requires_injected_token_before_transport():
    client = GitHubContentsClient(
        owner="example",
        repo="repository",
        landscape_path="landscape.json",
        token_provider=lambda: "",
    )

    try:
        client.read_repository_root()
    except Exception as exc:
        assert "GitHub token is not configured" in str(exc)
    else:
        raise AssertionError("missing GitHub token must prevent transport")

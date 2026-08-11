from github_repository_landscape import GitHubRepositoryLandscapeAdapter


class FakeRepositoryClient:
    def read_repository_root(self):
        return {
            "repository": "bxa05221-ux/shirakami-OS",
            "branch": "main",
            "entries": [
                {"name": "README.md", "path": "README.md", "type": "file"},
                {"name": "runtime", "path": "runtime", "type": "dir"},
            ],
        }


def test_repository_landscape_is_read_only_observation():
    adapter = GitHubRepositoryLandscapeAdapter(FakeRepositoryClient())
    state = adapter.read_state()

    assert state["repository"] == "bxa05221-ux/shirakami-OS"
    assert state["branch"] == "main"
    assert {entry["name"] for entry in state["entries"]} == {"README.md", "runtime"}

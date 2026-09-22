from pathlib import Path

from runtime.github_protocol_loader import GitHubProtocolLoader
from runtime.local_repository_loader import LocalRepositoryProtocolLoader


VALID_YAML = """\
matome:
  title: SHIRAKAMI LOCAL REPOSITORY
  version: "0.1"
  statement: >
    A local checkout provides the same protocol artifact without requiring
    the Runtime to depend on GitHub during execution.
pipeline:
  - phase: observe
    action: inspect
"""


class FakeGitHubContentsClient:
    def __init__(self, payload):
        self.payload = payload

    def get(self, path):
        return self.payload


def test_github_and_local_repository_loaders_produce_same_protocol(tmp_path: Path):
    protocol_path = "protocols/local-repository.yaml"
    local_path = tmp_path / protocol_path
    local_path.parent.mkdir(parents=True)
    local_path.write_text(VALID_YAML, encoding="utf-8")

    github_protocol = GitHubProtocolLoader(
        FakeGitHubContentsClient({"content": VALID_YAML})
    ).load(protocol_path)
    local_protocol = LocalRepositoryProtocolLoader(tmp_path).load(protocol_path)

    assert local_protocol == github_protocol
    assert local_protocol.title == "SHIRAKAMI LOCAL REPOSITORY"
    assert local_protocol.pipeline == (
        {"phase": "observe", "action": "inspect"},
    )

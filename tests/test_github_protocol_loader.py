from runtime.github_protocol_loader import GitHubProtocolLoader


class FakeGitHubContentsClient:
    def __init__(self, payload):
        self.payload = payload
        self.requested_path = None

    def get(self, path):
        self.requested_path = path
        return self.payload


def test_github_protocol_loader_delegates_yaml_to_existing_loader():
    yaml_text = """
matome:
  title: TSUGARU GUIDE HIGH SCHOOL
  version: "0.1"
pipeline:
  - question
  - fieldwalk
  - observation
"""
    client = FakeGitHubContentsClient({"content": yaml_text})

    protocol = GitHubProtocolLoader(client).load(
        "protocols/tsugaru-guide-highschool.yaml"
    )

    assert client.requested_path == "protocols/tsugaru-guide-highschool.yaml"
    assert protocol is not None


def test_github_protocol_loader_accepts_raw_text_payload():
    yaml_text = """
matome:
  title: TSUGARU GUIDE HIGH SCHOOL
  version: "0.1"
"""
    protocol = GitHubProtocolLoader(
        FakeGitHubContentsClient(yaml_text)
    ).load("protocols/tsugaru-guide-highschool.yaml")

    assert protocol is not None

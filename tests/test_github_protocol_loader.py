from runtime.github_protocol_loader import GitHubProtocolLoader


class FakeGitHubContentsClient:
    def __init__(self, payload):
        self.payload = payload
        self.requested_path = None

    def get(self, path):
        self.requested_path = path
        return self.payload


VALID_YAML = """
matome:
  title: TSUGARU GUIDE HIGH SCHOOL
  version: "0.1"
  statement: >
    Students observe the regional landscape and connect their observations to the community.
pipeline:
  - phase: question
    action: formulate_question
  - phase: fieldwalk
    action: observe_landscape
  - phase: observation
    action: record_observation
"""


def test_github_protocol_loader_delegates_yaml_to_existing_loader():
    client = FakeGitHubContentsClient({"content": VALID_YAML})

    protocol = GitHubProtocolLoader(client).load(
        "protocols/tsugaru-guide-highschool.yaml"
    )

    assert client.requested_path == "protocols/tsugaru-guide-highschool.yaml"
    assert protocol.title == "TSUGARU GUIDE HIGH SCHOOL"
    assert protocol.version == "0.1"
    assert protocol.pipeline[0] == {
        "phase": "question",
        "action": "formulate_question",
    }


def test_github_protocol_loader_accepts_raw_text_payload():
    protocol = GitHubProtocolLoader(
        FakeGitHubContentsClient(VALID_YAML)
    ).load("protocols/tsugaru-guide-highschool.yaml")

    assert protocol.title == "TSUGARU GUIDE HIGH SCHOOL"
    assert len(protocol.pipeline) == 3

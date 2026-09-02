from runtime.github_protocol_loader import GitHubProtocolLoader


class FakeGitHubContentsClient:
    def __init__(self, payload):
        self.payload = payload

    def get(self, path):
        assert path == "protocols/tsugaru-guide-highschool.yaml"
        return self.payload


def test_tsugaru_guide_protocol_can_cross_github_loader_boundary():
    yaml_text = """matome:
  title: TSUGARU GUIDE HIGH SCHOOL
  version: "0.1"
  statement: >
    地域を歩き、問いを持ち、観察し、記録する。
pipeline:
  - phase: question
    action: ask
  - phase: fieldwalk
    action: observe
  - phase: observation
    action: record
"""
    protocol = GitHubProtocolLoader(
        FakeGitHubContentsClient({"content": yaml_text})
    ).load("protocols/tsugaru-guide-highschool.yaml")

    assert protocol.title == "TSUGARU GUIDE HIGH SCHOOL"
    assert protocol.version == "0.1"
    assert "地域を歩き" in protocol.statement
    assert len(protocol.pipeline) == 3

from evidence import capture_evidence
from github_landscape_adapter import FakeGitHubClient, GitHubLandscapeAdapter
from prototype import Runtime, example_protocol


def test_github_adapter_maps_verified_transition_to_external_landscape():
    result = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "github landscape"},
    )
    evidence = capture_evidence(result)

    client = FakeGitHubClient()
    adapter = GitHubLandscapeAdapter(client)
    adapter.apply_transition(evidence)

    state = adapter.read_state()
    assert state["changed"] is True
    assert state["protocol_id"] == "example.protocol"
    assert state["input"]["message"] == "github landscape"


def test_github_adapter_does_not_write_failure_as_landscape_transition():
    def failing_protocol(context):
        raise RuntimeError("boom")

    result = Runtime().execute("failing.protocol", failing_protocol, {})
    evidence = capture_evidence(result)

    client = FakeGitHubClient()
    adapter = GitHubLandscapeAdapter(client)
    adapter.apply_transition(evidence)

    assert adapter.read_state() == {}

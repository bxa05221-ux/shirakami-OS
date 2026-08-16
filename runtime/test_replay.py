from evidence import capture_evidence
from landscape import LandscapeState
from prototype import Runtime, example_protocol
from projection import project_evidence
from replay import capture_replay, replay_matches


def run_once():
    result = Runtime().execute("example.protocol", example_protocol, {"message": "hello landscape"})
    evidence = capture_evidence(result)
    landscape = project_evidence(evidence)
    return capture_replay(result, evidence, landscape)


def test_execution_evidence_landscape_replay_is_deterministic():
    first = run_once()
    second = run_once()
    assert replay_matches(first, second)


def test_replay_fingerprints_are_distinct_for_different_inputs():
    a = Runtime().execute("example.protocol", example_protocol, {"message": "a"})
    b = Runtime().execute("example.protocol", example_protocol, {"message": "b"})
    assert capture_replay(a, capture_evidence(a), project_evidence(capture_evidence(a))).execution_fingerprint != capture_replay(
        b, capture_evidence(b), project_evidence(capture_evidence(b))
    ).execution_fingerprint

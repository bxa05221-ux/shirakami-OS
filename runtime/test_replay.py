from evidence import capture_evidence
from prototype import Runtime, example_protocol
from projection import project_evidence
from replay import capture_replay, replay_landscape, replay_matches


def run_once(message="hello landscape"):
    result = Runtime().execute("example.protocol", example_protocol, {"message": message})
    evidence = capture_evidence(result)
    landscape = project_evidence(evidence)
    return result, evidence, landscape


def test_execution_evidence_landscape_replay_is_deterministic():
    first_result, first_evidence, first_landscape = run_once()
    second_result, second_evidence, second_landscape = run_once()
    assert replay_matches(
        capture_replay(first_result, first_evidence, first_landscape),
        capture_replay(second_result, second_evidence, second_landscape),
    )


def test_replay_reconstructs_the_same_landscape():
    _, evidence, projected = run_once()
    assert replay_landscape([evidence]) == projected


def test_replay_fingerprints_are_distinct_for_different_inputs():
    a_result, a_evidence, a_landscape = run_once("a")
    b_result, b_evidence, b_landscape = run_once("b")
    assert capture_replay(a_result, a_evidence, a_landscape).execution_fingerprint != capture_replay(
        b_result, b_evidence, b_landscape
    ).execution_fingerprint

"""Regression tests for Evidence boundary freezing."""

from runtime.evidence import capture_evidence
from runtime.prototype import ExecutionResult, Transition


def make_result(data):
    return ExecutionResult(
        status="completed",
        protocol_id="evidence.freeze.regression",
        transition=Transition(kind="test.transition", data=data),
        signals=("transition.observed",),
        steps=1,
    )


def test_nested_mutable_values_are_detached_and_frozen():
    source = {
        "nested": {"items": ["before"]},
        "binary": bytearray(b"abc"),
        "view": memoryview(b"xyz"),
    }

    evidence = capture_evidence(make_result(source))
    source["nested"]["items"].append("after")
    source["binary"][0] = ord("z")

    assert evidence.transition_data["nested"]["items"] == ("before",)
    assert evidence.transition_data["binary"] == b"abc"
    assert evidence.transition_data["view"] == b"xyz"


def test_frozen_binary_values_cannot_be_mutated_in_place():
    evidence = capture_evidence(make_result({"binary": bytearray(b"abc")}))

    assert isinstance(evidence.transition_data["binary"], bytes)

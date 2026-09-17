from dataclasses import FrozenInstanceError

import pytest

from evidence import EvidenceRecord, _freeze, capture_evidence, is_transition_evidence
from prototype import Runtime, Transition, example_protocol


def test_successful_transition_becomes_immutable_evidence():
    result = Runtime().execute(
        "example.protocol",
        example_protocol,
        {"message": "hello landscape"},
    )

    evidence = capture_evidence(result)

    assert isinstance(evidence, EvidenceRecord)
    assert evidence.protocol_id == "example.protocol"
    assert evidence.status == "completed"
    assert evidence.transition_kind == "example.transition"
    assert evidence.transition_data["changed"] is True
    assert "transition.observed" in evidence.signals
    assert is_transition_evidence(evidence) is True

    with pytest.raises(TypeError):
        evidence.transition_data["changed"] = False

    with pytest.raises(FrozenInstanceError):
        evidence.status = "rewritten"


def test_failure_result_remains_observable_without_transition_evidence():
    def failing_protocol(context):
        raise RuntimeError("boom")

    result = Runtime().execute(
        "failing.protocol",
        failing_protocol,
        {},
    )

    evidence = capture_evidence(result)

    assert evidence.status == "failed"
    assert evidence.transition_kind == "execution.failed"
    assert evidence.transition_data["error_type"] == "RuntimeError"
    assert evidence.transition_data["message"] == "boom"
    assert is_transition_evidence(evidence) is False


def test_nested_evidence_data_is_deeply_immutable():
    frozen = _freeze(
        {
            "nested": {"items": [{"changed": True}]},
            "labels": ["observed"],
        }
    )

    with pytest.raises(TypeError):
        frozen["nested"]["items"][0]["changed"] = False

    with pytest.raises(TypeError):
        frozen["nested"]["items"] += ({"changed": False},)

    with pytest.raises(TypeError):
        frozen["labels"] += ("rewritten",)


def test_from_result_freezes_nested_transition_data():
    def nested_protocol(context):
        return Transition(
            kind="nested.transition",
            data={"payload": {"items": [{"value": 1}]}},
        )

    result = Runtime().execute("nested.protocol", nested_protocol, {})
    evidence = EvidenceRecord.from_result(result)

    with pytest.raises(TypeError):
        evidence.transition_data["payload"]["items"][0]["value"] = 2


def test_freezes_scalar_sets_as_frozensets():
    frozen = _freeze({"tags": {"observed", "verified"}})

    assert frozen["tags"] == frozenset({"observed", "verified"})
    assert isinstance(frozen["tags"], frozenset)

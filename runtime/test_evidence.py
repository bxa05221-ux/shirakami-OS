from dataclasses import FrozenInstanceError

import pytest

from evidence import EvidenceRecord, capture_evidence, is_transition_evidence
from prototype import Runtime, example_protocol


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
    assert len(evidence.evidence_id) == 64

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


def test_equivalent_evidence_has_stable_identity():
    first = EvidenceRecord(
        protocol_id="observed.protocol",
        status="observed",
        transition_kind="protocol.observed",
        transition_data={"protocol_path": "protocol.yaml"},
        signals=("PROTOCOL_ARTIFACT",),
    )
    second = EvidenceRecord(
        protocol_id="observed.protocol",
        status="observed",
        transition_kind="protocol.observed",
        transition_data={"protocol_path": "protocol.yaml"},
        signals=("PROTOCOL_ARTIFACT",),
    )

    assert first.evidence_id == second.evidence_id


def test_changed_evidence_changes_identity():
    first = EvidenceRecord(
        protocol_id="observed.protocol",
        status="observed",
        transition_kind="protocol.observed",
        transition_data={"protocol_path": "protocol.yaml"},
        signals=("PROTOCOL_ARTIFACT",),
    )
    changed = EvidenceRecord(
        protocol_id="observed.protocol",
        status="observed",
        transition_kind="protocol.observed",
        transition_data={"protocol_path": "other.yaml"},
        signals=("PROTOCOL_ARTIFACT",),
    )

    assert first.evidence_id != changed.evidence_id

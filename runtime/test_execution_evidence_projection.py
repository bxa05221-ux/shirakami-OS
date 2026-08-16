"""R0027.8 / R0027.9 boundary tests for Evidence and Projection."""

from pathlib import Path

from evidence import EvidenceRecord, capture_evidence
from projection import project_evidence
from prototype import Runtime
from protocol_bridge import protocol_from_ir
from protocol_loader import load_matome


PROTOCOL = Path(__file__).resolve().parents[1] / "protocols" / "manual" / "manga-user-manual.yaml"


def _execute():
    protocol = load_matome(PROTOCOL)
    runtime = Runtime()
    result = runtime.execute(
        protocol.protocol_id,
        protocol_from_ir(protocol),
        {"language": "ja"},
    )
    return protocol, result


def test_execution_to_evidence_is_deterministic():
    protocol, first = _execute()
    _, second = _execute()

    evidence_a = capture_evidence(first)
    evidence_b = capture_evidence(second)

    assert isinstance(evidence_a, EvidenceRecord)
    assert evidence_a == evidence_b
    assert evidence_a.protocol_id == protocol.protocol_id
    assert evidence_a.status == "completed"
    assert evidence_a.transition_kind == "matome.protocol.transition"
    assert evidence_a.transition_data == evidence_b.transition_data


def test_evidence_is_immutable():
    _, result = _execute()
    evidence = capture_evidence(result)

    try:
        evidence.status = "tampered"
    except Exception:
        pass
    else:
        raise AssertionError("EvidenceRecord must remain immutable")

    assert evidence.status == "completed"


def test_projection_is_separate_from_evidence_capture():
    _, result = _execute()
    evidence = capture_evidence(result)

    landscape_a = project_evidence(evidence)
    landscape_b = project_evidence(evidence)

    assert landscape_a == landscape_b
    assert landscape_a["protocol_id"] == evidence.protocol_id
    assert landscape_a["changed"] is True
    assert evidence.transition_data["changed"] is True

    # Projection returns a view; it does not mutate the immutable Evidence record.
    assert evidence.status == "completed"

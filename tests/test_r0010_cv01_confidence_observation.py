from runtime.evidence import EvidenceRecord
from runtime.landscape import LandscapeState
from runtime.projection import project_evidence
from runtime.replay import evidence_fingerprint, replay_landscape


def _evidence(confidence: str) -> EvidenceRecord:
    return EvidenceRecord(
        protocol_id="r0010-cv-01",
        status="observed",
        transition_kind="OBSERVE",
        transition_data={"changed": True, "scene": "same"},
        signals=("observation",),
        confidence=confidence,
    )


def test_r0010_cv01_confidence_is_retained_by_evidence():
    observed = _evidence("observed")
    provisional = _evidence("provisional")

    assert observed.confidence == "observed"
    assert provisional.confidence == "provisional"


def test_r0010_cv01_projection_does_not_expose_confidence():
    evidence = _evidence("provisional")
    projected = project_evidence(evidence, LandscapeState.empty())

    assert projected == {"changed": True, "scene": "same"}
    assert "confidence" not in projected


def test_r0010_cv01_replay_does_not_expose_confidence():
    evidence = _evidence("provisional")

    assert replay_landscape([evidence]) == {"changed": True, "scene": "same"}


def test_r0010_cv01_evidence_fingerprint_does_not_distinguish_confidence():
    observed = _evidence("observed")
    provisional = _evidence("provisional")

    assert evidence_fingerprint(observed) == evidence_fingerprint(provisional)

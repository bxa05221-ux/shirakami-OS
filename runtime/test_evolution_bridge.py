from evolution_bridge import (
    ContextSnapshot,
    EvidenceQuery,
    MismatchEvidence,
    ProtocolCandidate,
    VerificationResult,
    mismatch_to_evidence,
    transition_to_evidence,
)
from evidence import EvidenceRecord
from evolution_loop import EvidenceClass, EvolutionLoop


def test_transition_bridges_to_canonical_evidence():
    loop = EvolutionLoop()
    result = loop.dispatch("observe", {"observation": "new input"})
    assert result.accepted
    evidence = transition_to_evidence(loop.records[-1])
    assert isinstance(evidence, EvidenceRecord)
    assert evidence.protocol_id == "R0100"
    assert evidence.signals == ("OBSERVATION",)
    assert evidence.transition_data["from_state"] == "IDLE"


def test_rejected_transition_is_queryable_failure_evidence():
    loop = EvolutionLoop()
    result = loop.dispatch("execute")
    assert not result.accepted
    evidence = transition_to_evidence(loop.records[-1])
    assert evidence is not None
    query = EvidenceQuery([evidence])
    assert len(query.by_signal(EvidenceClass.FAILURE.value)) == 1


def test_context_candidate_and_verification_boundaries_are_explicit():
    snapshot = ContextSnapshot(
        landscape={"place": "test"},
        protocol_id="P001",
        runtime_state="READY",
        metadata={"source": "test"},
    )
    candidate = ProtocolCandidate(
        protocol_id="P002",
        diff_ref="D001",
        rationale="Mismatch requires revision",
        source_evidence=("E001",),
    )
    verification = VerificationResult(
        status="mismatch",
        uncertainty="medium",
        observed={"actual": "B", "expected": "A"},
    )
    assert snapshot.as_mapping()["runtime_state"] == "READY"
    assert candidate.diff_ref == "D001"
    assert verification.uncertainty == "medium"


def test_mismatch_evidence_preserves_expected_observed_boundary():
    mismatch = MismatchEvidence(
        protocol_id="P001",
        diff_ref="D001",
        expected="expected.transition",
        observed="actual.transition",
        uncertainty="medium",
        source_evidence=("EV-001",),
        context={"runtime_state": "VERIFY"},
    )
    evidence = mismatch_to_evidence(mismatch)
    assert evidence.status == "mismatch"
    assert evidence.signals == ("MISMATCH",)
    assert evidence.transition_data["expected"] == "expected.transition"
    assert evidence.transition_data["observed"] == "actual.transition"
    assert evidence.transition_data["uncertainty"] == "medium"
    assert evidence.transition_data["diff_ref"] == "D001"

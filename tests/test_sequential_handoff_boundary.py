from dataclasses import dataclass


@dataclass(frozen=True)
class Handoff:
    source: str
    target: str
    evidence: tuple[str, ...]


def test_sequential_handoff_preserves_evidence_and_role_boundary():
    handoff = Handoff(
        source="observer",
        target="auditor",
        evidence=("current_state: observed", "detected_gap: none"),
    )

    assert handoff.source == "observer"
    assert handoff.target == "auditor"
    assert handoff.evidence == (
        "current_state: observed",
        "detected_gap: none",
    )


def test_handoff_is_immutable_after_creation():
    handoff = Handoff(
        source="verifier",
        target="confirmer",
        evidence=("pass",),
    )

    try:
        handoff.evidence = ("changed",)
    except AttributeError:
        pass
    else:
        raise AssertionError("handoff evidence must remain immutable")

    assert handoff.evidence == ("pass",)

from runtime.evidence import capture_evidence
from runtime.i_field import IField, ImaginaryTerm
from runtime.prototype import Runtime, Transition
from runtime.replay import evidence_fingerprint


def test_r0113_evidence_identity_is_the_existing_content_fingerprint():
    result = Runtime().execute(
        "oppai.observation",
        lambda _context: Transition(
            kind="oppai.observation.recorded",
            data={"changed": True, "unresolved": ["what remains unknown?"]},
        ),
        {},
    )
    evidence = capture_evidence(result)

    evidence_ref = evidence_fingerprint(evidence)
    assert evidence_ref
    assert evidence_ref == evidence_fingerprint(evidence)

    field = IField((ImaginaryTerm("i-001", "left", "what remains unknown?"),))
    resolved = field.resolve(
        "i-001",
        evidence.transition_data["unresolved"][0],
        evidence_ref,
    )

    assert resolved.evidence_ref == evidence_ref
    assert field.unresolved_count() == 0


def test_r0113_different_evidence_has_a_different_identity():
    first = capture_evidence(
        Runtime().execute(
            "oppai.observation",
            lambda _context: Transition(
                kind="oppai.observation.recorded",
                data={"changed": True, "unresolved": ["first"]},
            ),
            {},
        )
    )
    second = capture_evidence(
        Runtime().execute(
            "oppai.observation",
            lambda _context: Transition(
                kind="oppai.observation.recorded",
                data={"changed": True, "unresolved": ["second"]},
            ),
            {},
        )
    )

    assert evidence_fingerprint(first) != evidence_fingerprint(second)

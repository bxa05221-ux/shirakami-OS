import pytest

from runtime.i_field import IField, ImaginaryTerm


def test_i_term_disappears_when_resolved_by_evidence():
    field = IField((ImaginaryTerm("i1", "left", "why is restructuring unacceptable?"),))

    assert field.unresolved_count() == 1
    resolved = field.resolve("i1", "workplace disclosure risk", "evidence-001")

    assert resolved.evidence_ref == "evidence-001"
    assert resolved.value == "workplace disclosure risk"
    assert field.unresolved_count() == 0
    assert field.is_resolved()


def test_new_i_can_appear_after_resolution():
    field = IField((ImaginaryTerm("i1", "left", "first unknown"),))
    field.resolve("i1", "resolved", "evidence-001")
    field.add(ImaginaryTerm("i2", "right", "new unknown in next state"))

    assert field.unresolved_count() == 1
    assert field.unresolved[0].term_id == "i2"


def test_resolution_requires_observable_evidence_reference():
    field = IField((ImaginaryTerm("i1", "right", "unknown"),))

    with pytest.raises(ValueError):
        field.resolve("i1", "guessed", "")

    assert field.unresolved_count() == 1


def test_i_remains_unresolved_until_all_required_evidence_is_available():
    field = IField(
        (
            ImaginaryTerm(
                "i1",
                "left",
                "what remains unorganized?",
                required_evidence=("evidence-001", "evidence-002"),
            ),
        )
    )

    available = {"evidence-001": "observed"}
    assert not field.can_resolve("i1", available)
    with pytest.raises(ValueError):
        field.resolve("i1", "guessed", "evidence-001", available)
    assert field.unresolved_count() == 1

    available["evidence-002"] = "observed"
    assert field.can_resolve("i1", available)
    resolved = field.resolve("i1", "resolved", "evidence-002", available)

    assert resolved.value == "resolved"
    assert field.unresolved_count() == 0
    assert field.is_resolved()

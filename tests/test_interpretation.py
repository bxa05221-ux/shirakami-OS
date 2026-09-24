from runtime.interpretation import InterpretationRecord


def test_interpretation_has_stable_distinct_identity():
    record = InterpretationRecord(
        actor_id="AI-A",
        source_evidence_ids=("e-001",),
        content="A possible interpretation",
    )
    same = InterpretationRecord(
        actor_id="AI-A",
        source_evidence_ids=("e-001",),
        content="A possible interpretation",
    )
    assert record.interpretation_id == same.interpretation_id
    assert record.interpretation_id != "e-001"


def test_interpretation_never_becomes_authority():
    record = InterpretationRecord(
        actor_id="AI-A",
        source_evidence_ids=("e-001",),
        content="A possible interpretation",
    )
    assert record.is_authority is False


def test_interpretation_requires_evidence_and_actor():
    try:
        InterpretationRecord(
            actor_id="",
            source_evidence_ids=(),
            content="x",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("invalid InterpretationRecord must fail closed")

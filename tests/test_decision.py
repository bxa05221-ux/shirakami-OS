from runtime.decision import DecisionRecord


def test_decision_has_stable_identity():
    record = DecisionRecord(
        actor_id="HUMAN-A",
        target_interpretation_id="i-001",
        timestamp="2026-09-24T12:00:00Z",
    )
    same = DecisionRecord(
        actor_id="HUMAN-A",
        target_interpretation_id="i-001",
        timestamp="2026-09-24T12:00:00Z",
    )
    assert record.decision_id == same.decision_id
    assert record.decision_id != "i-001"


def test_decision_requires_actor_and_target():
    try:
        DecisionRecord(
            actor_id="",
            target_interpretation_id="",
            timestamp="2026-09-24T12:00:00Z",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("DecisionRecord requires actor and target")


def test_decision_can_supersede_without_overwriting():
    record = DecisionRecord(
        actor_id="HUMAN-A",
        target_interpretation_id="i-001",
        timestamp="2026-09-24T12:00:00Z",
        supersedes="d-000",
    )
    assert record.supersedes == "d-000"

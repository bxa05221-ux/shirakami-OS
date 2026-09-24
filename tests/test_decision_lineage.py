from runtime.decision_lineage import DecisionLineage


def test_lineage_records_supersession_without_overwrite():
    lineage = DecisionLineage(
        decision_id="d-002",
        timestamp="2026-09-24T12:01:00Z",
        supersedes="d-001",
    )
    assert lineage.decision_id == "d-002"
    assert lineage.supersedes == "d-001"


def test_lineage_rejects_self_supersession():
    try:
        DecisionLineage(
            decision_id="d-001",
            timestamp="2026-09-24T12:01:00Z",
            supersedes="d-001",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("self-supersession must fail closed")

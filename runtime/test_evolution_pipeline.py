from evolution_bridge import ContextSnapshot, MismatchEvidence
from evolution_pipeline import EvidenceDrivenRuntime
from prototype import Transition


def test_end_to_end_cycle_reaches_accepted():
    app = EvidenceDrivenRuntime()
    app.observe(
        {"input": "hello"},
        ContextSnapshot(landscape={"place": "test"}, protocol_id="P1"),
    )
    analysis = app.analyze("P1")
    assert analysis.protocol_id == "P1"
    result = app.execute(
        lambda context: Transition("example.transition", {"changed": True}),
        "P1",
        {"input": "hello"},
    )
    verification = app.verify(result, expected_transition_kind="example.transition")
    assert verification.status == "pass"
    assert app.loop.state.value == "ACCEPTED"

    # The accepted cycle leaves observation, execution, and verification
    # as the canonical Evidence records. ContextSnapshot remains the
    # externalized execution context rather than a duplicate store record.
    records = app.store.all()
    assert len(records) == 3
    assert [record.transition_kind for record in records] == [
        "R0100:observe",
        "example.transition",
        "example.transition",
    ]


def test_new_protocol_requires_human_review_then_accepts():
    app = EvidenceDrivenRuntime()
    app.observe({"input": "new"}, ContextSnapshot(protocol_id="P2"))
    analysis = app.analyze("P2", protocol_exists=False, diff_ref="D001")
    assert analysis.candidate is not None
    assert analysis.candidate.diff_ref == "D001"
    assert app.loop.state.value == "HUMAN_REVIEW"

    assert app.approve(approved=True)
    assert app.loop.state.value == "READY"

    result = app.execute(
        lambda context: Transition("new.transition", {"changed": True}),
        "P2",
    )
    verification = app.verify(result, expected_transition_kind="new.transition")
    assert verification.status == "pass"
    assert app.loop.state.value == "ACCEPTED"
    assert any(r.signals == ("HUMAN_DECISION",) for r in app.store.all())


def test_human_review_rejects_without_execution():
    app = EvidenceDrivenRuntime()
    app.observe({"input": "new"}, ContextSnapshot(protocol_id="P3"))
    app.analyze("P3", protocol_exists=False)
    assert app.approve(approved=False)
    assert app.loop.state.value == "IDLE"


def test_mismatch_reenters_diff_and_externalizes_the_discrepancy():
    app = EvidenceDrivenRuntime()
    app.observe({"input": "hello"}, ContextSnapshot(protocol_id="P1"))
    app.analyze("P1")
    result = app.execute(
        lambda context: Transition("actual.transition", {"changed": True}),
        "P1",
    )
    verification = app.verify(
        result,
        expected_transition_kind="expected.transition",
        diff_ref="D001",
    )
    assert verification.status == "mismatch"
    assert app.loop.state.value == "DIFF"

    mismatches = [
        record for record in app.store.all()
        if record.signals == ("MISMATCH",)
    ]
    assert len(mismatches) >= 2
    formal = [
        record for record in mismatches
        if record.transition_kind == "R0100:mismatch"
    ][-1]
    assert formal.transition_data["expected"] == "expected.transition"
    assert formal.transition_data["observed"] == "actual.transition"
    assert formal.transition_data["diff_ref"] == "D001"
    assert formal.transition_data["uncertainty"] == "medium"

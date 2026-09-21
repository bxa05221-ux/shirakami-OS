from evolution_bridge import ContextSnapshot
from evolution_pipeline import EvidenceDrivenRuntime
from prototype import Transition


def test_end_to_end_cycle_reaches_accepted():
    app = EvidenceDrivenRuntime()
    app.observe({"input": "hello"}, ContextSnapshot(landscape={"place": "test"}, protocol_id="P1"))
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
    assert len(app.store.all()) >= 3


def test_mismatch_reenters_diff():
    app = EvidenceDrivenRuntime()
    app.observe({"input": "hello"}, ContextSnapshot(protocol_id="P1"))
    app.analyze("P1")
    app.approve()
    result = app.execute(
        lambda context: Transition("actual.transition", {"changed": True}),
        "P1",
    )
    verification = app.verify(result, expected_transition_kind="expected.transition")
    assert verification.status == "mismatch"
    assert app.loop.state.value == "DIFF"
    assert any(r.signals == ("MISMATCH",) for r in app.store.all())

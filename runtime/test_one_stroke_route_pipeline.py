from runtime.one_stroke_route_pipeline import OneStrokeRoutePipeline
from runtime.prototype import ExecutionContext, Transition
from runtime.evidence import EvidenceRecord


def _protocol(name, suffix):
    def run(context: ExecutionContext) -> Transition:
        value = context.input.get("value", "")
        return Transition(kind=f"step.{name}", data={"value": f"{value}{suffix}"})
    return run


def test_selected_route_requires_human_gate():
    pipeline = OneStrokeRoutePipeline()
    try:
        pipeline.select("route.demo", ("a", "b"), approved=False)
    except PermissionError:
        pass
    else:
        raise AssertionError("route selection must fail closed without approval")


def test_selected_route_runs_once_and_verifies_to_evidence():
    pipeline = OneStrokeRoutePipeline()
    selection = pipeline.select(
        "route.demo", ("a", "b", "c"), reviewer="human", approved=True
    )
    result = pipeline.execute(
        {
            "a": _protocol("a", "A"),
            "b": _protocol("b", "B"),
            "c": _protocol("c", "C"),
        },
        {"value": ""},
    )
    assert selection == result.selection
    assert result.execution.status == "completed"
    assert result.execution.transition.kind == "route.route.demo"
    assert result.execution.transition.data["route"] == ["a", "b", "c"]
    assert result.execution.transition.data["final"]["value"] == "ABC"
    assert result.verification.status == "pass"
    assert any(
        record.transition_kind == "route.route.demo" for record in result.evidence
    )


def test_selected_route_stops_on_missing_protocol():
    pipeline = OneStrokeRoutePipeline()
    pipeline.select("route.demo", ("a", "b"), approved=True)
    try:
        pipeline.execute({"a": _protocol("a", "A")})
    except KeyError as exc:
        assert "b" in str(exc)
    else:
        raise AssertionError("missing Protocol must stop execution")


def test_generated_candidate_flows_through_human_gate_runtime_and_evidence(tmp_path):
    from tools.protocol_route_candidates import generate_candidates

    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    a.write_text("title: A\noutput:\n  - shared\n", encoding="utf-8")
    b.write_text("title: B\ninput:\n  - shared\n", encoding="utf-8")

    pipeline = OneStrokeRoutePipeline()
    generated = generate_candidates([a, b], 2)
    assert generated == [(str(a), str(b))]

    selection = pipeline.select_candidate(
        "route.generated",
        generated[0],
        reviewer="human",
        approved=True,
    )
    result = pipeline.execute(
        {
            str(a): _protocol("a", "A"),
            str(b): _protocol("b", "B"),
        },
        {"value": ""},
    )
    assert selection.candidate == generated[0]
    assert result.execution.transition.data["route"] == list(generated[0])
    assert result.verification.status == "pass"
    assert any(
        record.transition_kind == "route.route.generated" for record in result.evidence
    )


def test_route_candidate_enters_evolution_loop_human_review_before_approval():
    pipeline = OneStrokeRoutePipeline()
    selection = pipeline.prepare_candidate(
        "route.loop",
        ("a", "b", "c"),
        reviewer="human",
    )

    assert selection.candidate == ("a", "b", "c")
    assert pipeline.runtime.loop.state.value == "HUMAN_REVIEW"
    assert not any(
        record.transition_kind == "route.route.loop"
        for record in pipeline.runtime.store.all()
    )


def test_evolution_loop_approval_then_one_stroke_execution_and_evidence():
    pipeline = OneStrokeRoutePipeline()
    pipeline.prepare_candidate(
        "route.loop",
        ("a", "b", "c"),
        reviewer="human",
    )

    selection = pipeline.approve_candidate(approved=True)
    assert selection.candidate == ("a", "b", "c")
    assert pipeline.runtime.loop.state.value == "READY"

    result = pipeline.execute(
        {
            "a": _protocol("a", "A"),
            "b": _protocol("b", "B"),
            "c": _protocol("c", "C"),
        },
        {"value": ""},
    )

    assert result.verification.status == "pass"
    assert pipeline.runtime.loop.state.value == "ACCEPTED"
    assert result.execution.transition.data["route"] == ["a", "b", "c"]
    assert any(
        record.transition_kind == "route.route.loop"
        for record in result.evidence
    )
    human_decisions = [
        record for record in pipeline.runtime.store.all()
        if record.signals == ("HUMAN_DECISION",)
    ]
    assert human_decisions


def test_evolution_loop_mismatch_does_not_advance_to_accepted():
    pipeline = OneStrokeRoutePipeline()
    pipeline.prepare_candidate("route.loop", ("a", "b"), reviewer="human")
    pipeline.approve_candidate(approved=True)

    result = pipeline.runtime.execute(
        lambda context: Transition("unexpected.transition", {"changed": True}),
        "route.loop",
        {"value": ""},
    )
    verification = pipeline.runtime.verify(
        result,
        expected_transition_kind="route.expected",
        diff_ref="route.loop",
    )

    assert verification.status == "mismatch"
    assert pipeline.runtime.loop.state.value == "DIFF"
    assert not any(
        record.transition_kind == "route.route.loop"
        and record.status == "completed"
        for record in pipeline.runtime.store.all()
    )



def test_evidence_derives_structural_candidates_without_authorization(tmp_path):
    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    a.write_text("title: A\noutput:\n  - shared\n", encoding="utf-8")
    b.write_text("title: B\ninput:\n  - shared\n", encoding="utf-8")

    evidence = (
        EvidenceRecord(
            protocol_id="observed.a",
            status="observed",
            transition_kind="protocol.observed",
            transition_data={"protocol_path": str(a)},
            signals=("PROTOCOL_ARTIFACT",),
        ),
        EvidenceRecord(
            protocol_id="observed.b",
            status="observed",
            transition_kind="protocol.observed",
            transition_data={"protocol_path": str(b)},
            signals=("PROTOCOL_ARTIFACT",),
        ),
    )

    pipeline = OneStrokeRoutePipeline()
    candidates = pipeline.propose_candidates_from_evidence(evidence, n=2)

    assert candidates == [(str(a), str(b))]
    assert pipeline.runtime.loop.state.value == "IDLE"


def test_evidence_candidate_requires_explicit_human_gate(tmp_path):
    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    a.write_text("title: A\noutput:\n  - shared\n", encoding="utf-8")
    b.write_text("title: B\ninput:\n  - shared\n", encoding="utf-8")

    evidence = (
        EvidenceRecord(
            protocol_id="observed.a",
            status="observed",
            transition_kind="protocol.observed",
            transition_data={"protocol_path": str(a)},
            signals=("PROTOCOL_ARTIFACT",),
        ),
        EvidenceRecord(
            protocol_id="observed.b",
            status="observed",
            transition_kind="protocol.observed",
            transition_data={"protocol_path": str(b)},
            signals=("PROTOCOL_ARTIFACT",),
        ),
    )

    pipeline = OneStrokeRoutePipeline()
    candidate = pipeline.propose_candidates_from_evidence(evidence, n=2)[0]
    selection = pipeline.prepare_candidate("route.evidence", candidate)

    assert selection.candidate == candidate
    assert pipeline.runtime.loop.state.value == "HUMAN_REVIEW"

    try:
        pipeline.execute({})
    except RuntimeError as exc:
        assert "not authorized" in str(exc)
    else:
        raise AssertionError("Evidence-derived candidate must not authorize execution")

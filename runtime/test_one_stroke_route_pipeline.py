from runtime.one_stroke_route_pipeline import OneStrokeRoutePipeline
from runtime.prototype import ExecutionContext, Transition


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


def test_generated_candidate_flows_through_human_gate_runtime_and_evidence():
    from tools.protocol_route_candidates import generate_candidates
    from pathlib import Path

    pipeline = OneStrokeRoutePipeline()
    generated = generate_candidates(
        [Path("protocols/a.yaml"), Path("protocols/b.yaml")], 2
    )
    assert generated == [("protocols/a.yaml", "protocols/b.yaml")]

    selection = pipeline.select_candidate(
        "route.generated",
        generated[0],
        reviewer="human",
        approved=True,
    )
    result = pipeline.execute(
        {
            "protocols/a.yaml": _protocol("a", "A"),
            "protocols/b.yaml": _protocol("b", "B"),
        },
        {"value": ""},
    )
    assert selection.candidate == generated[0]
    assert result.execution.transition.data["route"] == list(generated[0])
    assert result.verification.status == "pass"
    assert any(record.transition_kind == "route.route.generated" for record in result.evidence)

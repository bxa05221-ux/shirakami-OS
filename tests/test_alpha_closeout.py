from __future__ import annotations

from runtime.landscape import LandscapeState
from runtime.protocol_applicability import evaluate_applicability
from runtime.protocol_input import ProtocolInput
from runtime.prototype import Runtime, Transition, failing_protocol
from runtime.evidence import capture_evidence


def test_missing_source_is_preserved_as_unresolved_question() -> None:
    from runtime.project_landscape_assembly import assemble_landscape
    from runtime.project_landscape_loader import load_landscape
    from runtime.source_registry import build_registry

    registry = build_registry(
        [
            {
                "id": "missing-source",
                "type": "implementation",
                "path": "missing.json",
                "status": "active",
                "authority": "test",
            }
        ]
    )
    loaded = load_landscape(registry, {})
    landscape = assemble_landscape(loaded.sources, loaded.unresolved_questions)

    assert landscape.sources == ()
    assert landscape.unresolved_questions == ("source content unavailable: missing-source",)


def test_unresolved_applicability_does_not_change_landscape() -> None:
    context = ProtocolInput(
        context_id="s1",
        parent_landscape_ref="landscape-1",
        source_refs=(),
        unresolved_questions=(),
    )
    result = evaluate_applicability(
        context,
        "test.protocol",
        {"mode": "ready"},
        available={},
    )

    state = LandscapeState.from_snapshot({"scene_id": "dogfight", "turn_count": 0})
    before = state.snapshot()

    assert result.applicable is False
    assert result.unresolved_questions == ("condition unavailable: mode",)
    assert state.snapshot() == before
    assert state.evidence == []


def test_failed_applicability_does_not_change_landscape() -> None:
    context = ProtocolInput(
        context_id="s1",
        parent_landscape_ref="landscape-1",
        source_refs=(),
        unresolved_questions=(),
    )
    result = evaluate_applicability(
        context,
        "test.protocol",
        {"mode": "ready"},
        available={"mode": "blocked"},
    )

    state = LandscapeState.from_snapshot({"scene_id": "dogfight", "turn_count": 0})
    before = state.snapshot()

    assert result.applicable is False
    assert result.failed_conditions == ("mode",)
    assert state.snapshot() == before
    assert state.evidence == []


def test_runtime_failure_produces_failure_evidence_without_landscape_change() -> None:
    runtime = Runtime()
    result = runtime.execute("test.failing", failing_protocol, {"text": "x"})
    evidence = capture_evidence(result)
    state = LandscapeState.from_snapshot({"scene_id": "dogfight", "turn_count": 0})
    before = state.snapshot()

    state.apply_evidence(evidence)

    assert result.status == "failed"
    assert result.transition.kind == "execution.failed"
    assert evidence.status == "failed"
    assert evidence.protocol_id == "test.failing"
    assert state.snapshot() == before
    assert state.evidence == []


def test_completed_transition_is_applied_and_preserved_as_evidence() -> None:
    runtime = Runtime()

    def protocol(_context) -> Transition:
        return Transition(
            kind="test.turn_added",
            data={"changed": True, "text": "歩いてみる", "turn_count": 1},
        )

    result = runtime.execute("test.completed", protocol, {})
    evidence = capture_evidence(result)
    state = LandscapeState.from_snapshot({"scene_id": "dogfight", "turn_count": 0})

    state.apply_evidence(evidence)

    assert result.status == "completed"
    assert evidence.status == "completed"
    assert evidence.protocol_id == "test.completed"
    assert evidence.transition_kind == "test.turn_added"
    assert evidence.transition_data["text"] == "歩いてみる"
    assert state.snapshot()["turn_count"] == 1
    assert state.snapshot()["text"] == "歩いてみる"
    assert state.evidence == [evidence]

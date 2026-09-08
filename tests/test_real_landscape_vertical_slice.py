"""Real Landscape vertical slice using the committed Dogfight fixture."""
from __future__ import annotations

import json
from pathlib import Path

from runtime.context_boundary import create_context_snapshot
from runtime.landscape import LandscapeState
from runtime.project_landscape_assembly import assemble_landscape
from runtime.project_landscape_loader import load_landscape
from runtime.protocol_applicability import evaluate_applicability
from runtime.protocol_input import create_protocol_input
from runtime.protocol_ir import build_protocol_ir
from runtime.protocol_runtime import execute_protocol_ir
from runtime.prototype import Transition
from runtime.source_registry import build_registry
from runtime.thread_rpg import ThreadRenderer, ThreadRuntime


FIXTURE = Path(__file__).parent / "fixtures" / "dogfight_scene.json"


def test_real_landscape_reaches_thread_renderer() -> None:
    scene = json.loads(FIXTURE.read_text(encoding="utf-8"))
    refs = build_registry(
        [
            {
                "id": "dogfight.scene",
                "type": "implementation",
                "path": "tests/fixtures/dogfight_scene.json",
                "status": "active",
                "authority": "fixture",
                "requested_context": "writer-support",
            }
        ]
    )

    loaded = load_landscape(refs, {"dogfight.scene": scene})
    assert not loaded.unresolved_questions
    assert loaded.sources[0].content["scene_id"] == "dogfight-prologue-to-epilogue"

    landscape = assemble_landscape(loaded.sources, loaded.unresolved_questions)
    context = create_context_snapshot(
        landscape,
        context_id="ctx-dogfight",
        parent_landscape_ref="landscape-dogfight",
        requested_context="writer-support",
    )
    protocol_input = create_protocol_input(context)

    applicability = evaluate_applicability(
        protocol_input,
        "writer-support.transition",
        {"scene_type": "written_scene"},
        available={"scene_type": scene["type"]},
    )
    assert applicability.applicable

    protocol_ir = build_protocol_ir(
        protocol_input,
        protocol_id="writer-support.transition",
        transition_kind="writer-support.observation-enriched",
        transition_data={
            "changed": True,
            "scene_id": scene["scene_id"],
            "observation_count": len(scene["observations"]),
            "unresolved_question_count": len(scene["unresolved_questions"]),
        },
    )

    def declared_transition(_context) -> Transition:
        return Transition(kind=protocol_ir.transition_kind, data=protocol_ir.transition_data)

    execution = execute_protocol_ir(protocol_ir, declared_transition)
    assert execution.result.status == "completed"
    assert execution.evidence.transition_data["changed"] is True

    state = LandscapeState.empty()
    state.apply_evidence(execution.evidence)
    snapshot = state.snapshot()
    assert snapshot["scene_id"] == scene["scene_id"]
    assert snapshot["observation_count"] == 13
    assert snapshot["unresolved_question_count"] == 5

    thread_runtime = ThreadRuntime(response_adapter=lambda text, _state: f"echo: {text}")
    thread = thread_runtime.create_session("landscape-dogfight")
    turn, thread_state, thread_evidence = thread_runtime.submit_turn(
        thread.session_id,
        "このLandscapeをThreadとして歩いてみる。",
    )
    rendered = ThreadRenderer.render(thread_state)

    assert turn.response.startswith("echo:")
    assert thread_evidence.transition_kind == "thread.turn_added"
    assert rendered["landscape_ref"] == "landscape-dogfight"
    assert len(rendered["turns"]) == 1

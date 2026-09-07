"""Real-Landscape vertical slice for the Thread RPG 3.2 MVP boundary."""

from runtime.thread_rpg import (
    AnonymousOpinion,
    ThreadRenderer,
    ThreadRuntime,
)


LANDSCAPE_REF = "landscape://thread-rpg-mvp/demo"


def test_thread_rpg_real_landscape_vertical_slice():
    runtime = ThreadRuntime(response_adapter=lambda value, _state: f"echo: {value}")

    state = runtime.create_session(LANDSCAPE_REF)
    assert state.landscape_ref == LANDSCAPE_REF
    assert state.snapshot()["landscape_ref"] == LANDSCAPE_REF

    turn1, state, evidence1 = runtime.submit_turn(
        state.session_id,
        "今日はこの景色から始めたい。",
    )
    assert len(state.turns) == 1
    assert evidence1.transition_kind == "thread.turn_added"
    assert evidence1.transition_data["changed"] is True
    assert evidence1.transition_data["turn_count"] == 1

    turn2, state, evidence2 = runtime.submit_turn(
        state.session_id,
        "もう一つ、気になっていることがある。",
    )
    assert len(state.turns) == 2
    assert turn1.turn_id != turn2.turn_id
    assert evidence2.transition_kind == "thread.turn_added"
    assert evidence2.transition_data["turn_count"] == 2
    assert len(runtime.evidence(state.session_id)) == 2

    rendered = ThreadRenderer.render(state)
    assert rendered["landscape_ref"] == LANDSCAPE_REF
    assert len(rendered["turns"]) == 2


def test_thread_rpg_anonymous_group_projects_declared_weights_into_seven():
    opinions = [
        AnonymousOpinion("a", "こちらを試してみよう", 0.70),
        AnonymousOpinion("b", "いや、こちらも捨てがたい", 0.25),
        AnonymousOpinion("c", "少数だけど気になる", 0.05),
    ]

    rendered = ThreadRenderer.render_anonymous_group(opinions)

    assert len(rendered) == 7
    counts = {opinion_id: sum(item["opinion_id"] == opinion_id for item in rendered)
              for opinion_id in ("a", "b", "c")}
    assert sum(counts.values()) == 7
    assert all(count > 0 for count in counts.values())

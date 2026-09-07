"""Concrete behavior tests for the Thread RPG 3.2 runtime slice."""

from runtime.thread_rpg import ThreadRenderer, ThreadRuntime


def test_session_and_turn_produce_observable_state_and_evidence():
    runtime = ThreadRuntime(response_adapter=lambda text, _state: f"AI:{text}")
    state = runtime.create_session("landscape:test")

    turn, updated, evidence = runtime.submit_turn(state.session_id, "こんにちは")

    assert turn.input == "こんにちは"
    assert turn.response == "AI:こんにちは"
    assert len(updated.turns) == 1
    assert evidence.transition_kind == "thread.turn_added"
    assert evidence.transition_data["changed"] is True
    assert len(runtime.evidence(state.session_id)) == 1


def test_renderer_does_not_replace_runtime_state():
    runtime = ThreadRuntime()
    state = runtime.create_session("landscape:test")
    runtime.submit_turn(state.session_id, "test")

    rendered = ThreadRenderer.render(state)

    assert rendered["session_id"] == state.session_id
    assert len(rendered["turns"]) == 1
    assert rendered["turns"][0]["input"] == "test"
    assert len(state.evidence) == 1


def test_unresolved_question_can_remain_unanswered():
    runtime = ThreadRuntime()
    state = runtime.create_session("landscape:test")
    state.unresolved_questions.append("これはまだ分からない？")

    runtime.submit_turn(state.session_id, "分からないままにしておく")

    assert "これはまだ分からない？" in state.unresolved_questions

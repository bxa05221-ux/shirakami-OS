from runtime.threadrpg_v4_hanaichimonme_flow import HanaichimonmeSessionStore
from runtime.threadrpg_v4_minimal_flow import AnonymousReply, ReplyProposal
from runtime.wayfinding_api import execute_hanaichimonme_request


def _generator(thread, event):
    if event.kind == "post":
        return ReplyProposal((
            AnonymousReply(">>1 いや、その前提は訂正したい"),
            AnonymousReply("横からだけど、研究へ戻って検証しよう"),
        ))
    return ReplyProposal((AnonymousReply("続きの横レス"),))


def test_dynamic_selection_is_connected_to_generated_posts_and_session_history():
    session = HanaichimonmeSessionStore().get("hana-v4")
    first = session.generate("仮説を出す", _generator)
    second = session.generate("/next", _generator)

    generated_ids = [post.participant_id for post in first.thread.posts[1:]]
    assert set(generated_ids).issubset(set(first.plan.participant_ids))
    assert len(first.plan.participant_ids) < 7  # non-participation is normal
    assert any(link.relation == "reply" for link in first.semantic_history)
    assert any(link.relation == "correction" for link in first.semantic_history)
    assert any(link.relation == "cue" for link in first.semantic_history)
    assert second.thread.posts[: len(first.thread.posts)] == first.thread.posts


def test_same_anonymous_can_speak_twice_and_cue_changes_selection_without_fixed_roles():
    session = HanaichimonmeSessionStore().get("repeat")
    first = session.generate("話題", _generator)
    second = session.generate("/next", _generator)
    assert first.thread.posts[1].participant_id in [post.participant_id for post in second.thread.posts]
    assert second.plan.cue_detected is True
    assert first.human_gate_required is True
    assert first.reality_mutation_permitted is False


def test_transport_path_returns_generated_posts_and_keeps_session_state():
    sessions = HanaichimonmeSessionStore()
    first = execute_hanaichimonme_request(
        {"thread_id": "transport", "input": "相談"}, _generator, sessions
    )
    second = execute_hanaichimonme_request(
        {"thread_id": "transport", "input": "/next"}, _generator, sessions
    )
    assert first["posts"][1]["participant_id"] in first["selected_anonymous_speakers"]
    assert len(second["posts"]) > len(first["posts"])
    assert second["human_gate_required"] is True
    assert second["reality_mutation_permitted"] is False

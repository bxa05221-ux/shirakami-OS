"""Regression coverage for the v4 explicit post -> replies -> /next flow."""

import pytest

from runtime.aats import Thread
from runtime.threadrpg_v4_minimal_flow import (
    AnonymousReply,
    ReplyProposal,
    run_minimal_flow,
)


class DeterministicReplyGenerator:
    """Test-only local generator.  It is deliberately not an LLM connection."""

    def __call__(self, thread, event):
        if event.kind == "post":
            return ReplyProposal((
                AnonymousReply("それは気になる", (0,)),
                AnonymousReply("急いで決めなくていい", (0,)),
            ), unresolved_post_indices=(0,))
        return ReplyProposal((
            AnonymousReply("続きが聞きたい"),
            AnonymousReply("別の見方もあるかも"),
            AnonymousReply("今のままでもよさそう"),
        ))


def test_post_replies_and_explicit_next_form_one_traceable_flow():
    generator = DeterministicReplyGenerator()
    first = run_minimal_flow(Thread("t1"), "あの子が気になる", generator)
    second = run_minimal_flow(first.thread, "/next", generator)

    assert first.event.kind == "post"
    assert [post.participant_id for post in first.thread.posts] == ["icchi", "nanashi", "nanashi"]
    assert [reply.text for reply in first.replies] == ["それは気になる", "急いで決めなくていい"]
    assert [(item.post_index, item.text) for item in first.unresolved_questions] == [
        (0, "あの子が気になる")
    ]
    assert second.event.kind == "continue"
    assert second.event.text is None
    assert [post.participant_id for post in second.thread.posts] == [
        "icchi", "nanashi", "nanashi", "nanashi", "nanashi", "nanashi"
    ]
    assert len(second.replies) == 3  # no fixed four-reply requirement


def test_anonymous_replies_remain_non_authoritative_and_source_addressable():
    result = run_minimal_flow(Thread("t1"), "迷っている", DeterministicReplyGenerator())

    assert result.replies[0].source_post_indices == (0,)
    assert [(item.participant_id, item.text) for item in result.source_posts] == [
        ("icchi", "迷っている"),
        ("nanashi", "それは気になる"),
        ("nanashi", "急いで決めなくていい"),
    ]
    assert result.human_gate_required is True
    assert result.reality_mutation_permitted is False
    assert result.llm_connected is False


def test_generator_is_not_forced_to_answer_icchi_or_summarize():
    def side_conversation(_thread, _event):
        return ReplyProposal((
            AnonymousReply("映画の話にしよう"),
            AnonymousReply("それなら週末かな"),
        ))

    result = run_minimal_flow(Thread("t1"), "相談がある", side_conversation)

    assert [reply.text for reply in result.replies] == ["映画の話にしよう", "それなら週末かな"]


@pytest.mark.parametrize(
    "proposal",
    [
        ReplyProposal(()),
        ReplyProposal((AnonymousReply("a"),) * 9),
        ReplyProposal((AnonymousReply("a", (1,)),)),
        ReplyProposal((AnonymousReply("a"),), unresolved_post_indices=(1,)),
    ],
)
def test_invalid_reply_counts_or_future_provenance_are_rejected(proposal):
    with pytest.raises(ValueError):
        run_minimal_flow(Thread("t1"), "/next", lambda _thread, _event: proposal)


def test_missing_or_unknown_input_never_invokes_generation():
    def should_not_run(_thread, _event):
        raise AssertionError("generator must not run")

    with pytest.raises(ValueError):
        run_minimal_flow(Thread("t1"), None, should_not_run)
    with pytest.raises(ValueError):
        run_minimal_flow(Thread("t1"), "/stop", should_not_run)

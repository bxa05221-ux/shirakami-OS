"""Focused tests for the v4 input-to-thread boundary."""
import pytest

from runtime.aats import Thread
from runtime.threadrpg_v4_turn import advance_turn, append_generated_replies


def test_normal_post_records_only_real_human_text():
    result = advance_turn(Thread("t1"), "あの子のこと")
    assert result.event.kind == "post"
    assert result.thread.posts[0].participant_id == "icchi"
    assert result.thread.posts[0].text == "あの子のこと"


@pytest.mark.parametrize("raw", ["/next", "", "  "])
def test_continue_does_not_invent_human_post(raw):
    initial = Thread("t1")
    result = advance_turn(initial, raw)
    assert result.event.kind == "continue"
    assert result.event.text is None
    assert result.thread == initial
    assert result.generate_replies


def test_missing_input_does_not_advance():
    with pytest.raises(ValueError):
        advance_turn(Thread("t1"), None)


def test_generated_batch_is_bounded_and_preserves_order():
    thread = advance_turn(Thread("t1"), "test").thread
    updated = append_generated_replies(thread, ["好きなんじゃね？", "紹介しろ"])
    assert [p.participant_id for p in updated.posts] == ["icchi", "nanashi", "nanashi"]
    assert len(thread.posts) == 1


@pytest.mark.parametrize("replies", [[], [""] , ["a"] * 9])
def test_invalid_batch_is_rejected(replies):
    with pytest.raises(ValueError):
        append_generated_replies(Thread("t1"), replies)


def test_unknown_command_is_not_a_human_post():
    with pytest.raises(ValueError):
        advance_turn(Thread("t1"), "/pause")

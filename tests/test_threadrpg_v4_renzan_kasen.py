"""Regression tests for the isolated ThreadRPG -> Renzan/Kasen adapter."""

import pytest

from runtime.aats import Post, Thread
from runtime.threadrpg_v4_renzan_kasen import connect_thread


def sample_thread() -> Thread:
    return (
        Thread("thread-1")
        .with_post(Post("icchi", "私は今は決められない", "(._.)"))
        .with_post(Post("nanashi", "もう決めた方がいい"))
        .with_post(Post("nanashi", "急がなくていい"))
    )


def test_connection_preserves_original_posts_alongside_renzan_kasen_output():
    thread = sample_thread()
    original = thread.snapshot()

    result = connect_thread(thread)

    assert thread.snapshot() == original
    assert [(post.participant_id, post.text, post.aa) for post in result.source_posts] == [
        ("icchi", "私は今は決められない", "(._.)"),
        ("nanashi", "もう決めた方がいい", None),
        ("nanashi", "急がなくていい", None),
    ]
    assert [(viewpoint.participant_id, viewpoint.text, viewpoint.aa) for viewpoint in result.viewpoints] == [
        ("icchi", "私は今は決められない", "(._.)"),
        ("nanashi", "もう決めた方がいい", None),
        ("nanashi", "急がなくていい", None),
    ]
    assert "私は今は決められない" in result.narrative


def test_explicit_conflict_and_unresolved_question_remain_source_addressable():
    result = connect_thread(
        sample_thread(),
        conflict_pairs=((1, 2),),
        unresolved_post_indices=(0,),
    )

    assert [(item.left.post_index, item.right.post_index) for item in result.conflicts] == [(1, 2)]
    assert result.conflicts[0].left.text == "もう決めた方がいい"
    assert result.conflicts[0].right.text == "急がなくていい"
    assert [(item.post_index, item.text) for item in result.unresolved_questions] == [
        (0, "私は今は決められない")
    ]


@pytest.mark.parametrize(
    ("conflict_pairs", "unresolved_indices"),
    [
        (((0, 0),), ()),
        (((0, 3),), ()),
        ((), (3,)),
    ],
)
def test_invalid_references_are_rejected(conflict_pairs, unresolved_indices):
    with pytest.raises((IndexError, ValueError)):
        connect_thread(
            sample_thread(),
            conflict_pairs=conflict_pairs,
            unresolved_post_indices=unresolved_indices,
        )


def test_empty_thread_is_structured_without_fabricating_content():
    result = connect_thread(Thread("empty"))

    assert result.source_posts == ()
    assert result.viewpoints == ()
    assert result.narrative == ""
    assert result.conflicts == ()
    assert result.unresolved_questions == ()


def test_adapter_does_not_infer_conflict_or_question_from_text():
    result = connect_thread(sample_thread())

    assert result.conflicts == ()
    assert result.unresolved_questions == ()

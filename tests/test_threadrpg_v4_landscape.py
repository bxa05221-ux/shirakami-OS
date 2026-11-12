"""Five-turn differential layers preserve provenance and unresolved inquiry."""
import pytest

from runtime.aats import Post, Thread
from runtime.threadrpg_v4_landscape import ConversationLandscape, Delta


def test_five_generation_turns_create_a_layer_without_touching_thread():
    thread = Thread("t").with_post(Post("icchi", "まだ決めていない"))
    original = thread.snapshot()
    landscape = ConversationLandscape()
    for i in range(5):
        deltas = (Delta("question", f"問い{i}", (0,)),) if i == 0 else ()
        landscape = landscape.record_generation_turn(thread, deltas)
    assert landscape.generation_turns == 5
    assert len(landscape.layers) == 1
    assert (landscape.layers[0].turn_from, landscape.layers[0].turn_to) == (1, 5)
    assert landscape.layers[0].unresolved[0].content == "問い0"
    assert thread.snapshot() == original


def test_sixth_turn_stays_pending_and_unresolved_is_retained():
    thread = Thread("t").with_post(Post("icchi", "保留"))
    state = ConversationLandscape()
    for _ in range(5):
        state = state.record_generation_turn(thread)
    state = state.record_generation_turn(thread, (Delta("uncertainty", "未確認", (0,)),))
    assert len(state.layers) == 1
    assert state.unresolved_questions()[0].content == "未確認"


def test_matome_draft_distinguishes_observation_and_interpretation():
    thread = Thread("t").with_post(Post("icchi", "statement"))
    state = ConversationLandscape().record_generation_turn(
        thread,
        (
            Delta("observation", "reported statement", (0,),
                  origin="human_post", verified=True),
            Delta("interpretation", "possible meaning", (0,)),
            Delta("question", "open question", (0,)),
        ),
    )
    assert state.to_matome_draft() == {
        "facts": ["reported statement"],
        "interpretations": ["possible meaning"],
        "unresolved": ["open question"],
        "unverified": [],
    }


def test_missing_source_rejected_without_mutation():
    original = ConversationLandscape()
    with pytest.raises(ValueError):
        original.record_generation_turn(Thread("t"), (Delta("question", "問", (0,)),))
    assert original.generation_turns == 0


def test_not_every_five_posts_only_five_explicit_generations():
    thread = Thread("t").with_post(Post("icchi", "開始"))
    state = ConversationLandscape()
    for _ in range(4):
        state = state.record_generation_turn(thread)
    assert not state.layers
    assert state.generation_turns == 4

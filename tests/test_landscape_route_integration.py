"""Integration check for the shared Landscape entry point.

This test intentionally keeps Renzan/Kasen and Thread RPG separate. It verifies
only that the same Landscape reference can enter the one-person wayfinding path
and the multi-perspective Thread path without either renderer owning Landscape
semantics.
"""

from runtime.aats import Participant, Post, Thread
from runtime.thread_rpg import ThreadRuntime
from runtime.way import Kasen, Renzan


LANDSCAPE_REF = "landscape://shared-route/demo"


def test_same_landscape_supports_one_person_and_thread_paths():
    landscape = {"place": "current", "question": "どこから始める？"}

    # One-person path: AATS -> Renzan -> Kasen.
    one_person_thread = (
        Thread("one-person")
        .with_participant(Participant("human"))
        .with_post(Post("human", landscape["question"]))
    )
    viewpoints = Renzan().collect(one_person_thread)
    narrative = Kasen().compose(viewpoints)

    # Multi-perspective path: the same Landscape enters Thread RPG.
    runtime = ThreadRuntime(response_adapter=lambda value, _state: value)
    state = runtime.create_session(LANDSCAPE_REF)
    turn, state, evidence = runtime.submit_turn(
        state.session_id,
        landscape["question"],
    )

    assert narrative == landscape["question"]
    assert state.landscape_ref == LANDSCAPE_REF
    assert turn.input == landscape["question"]
    assert evidence.transition_kind == "thread.turn_added"
    assert evidence.transition_data["changed"] is True

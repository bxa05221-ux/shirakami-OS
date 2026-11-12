from runtime.aats import Thread
from runtime.evidence_store import EvidenceStore
from runtime.threadrpg_v4_minimal_flow import (
    AnonymousReply, ReplyProposal, run_minimal_flow
)
from runtime.threadrpg_v4_observation import (
    observe_post, record_observation
)
from runtime.threadrpg_v4_landscape import (
    ConversationLandscape, Delta
)
from runtime.threadrpg_v4_renzan_kasen import connect_thread


def generator(thread, event):
    if event.kind == "post":
        return ReplyProposal((
            AnonymousReply("interesting", (0,)),
            AnonymousReply(">>2 why?"),
        ), unresolved_post_indices=(0,))

    return ReplyProposal((
        AnonymousReply("no conclusion"),
        AnonymousReply("another viewpoint"),
        AnonymousReply("continue"),
    ))


def test_five_turn_integration():
    thread = Thread("integration-regression")
    store = EvidenceStore()
    landscape = ConversationLandscape()
    recorded_count = 0

    for turn_number, raw_input in enumerate(
        ("question", "/next", "/next", "/next", "/next"), 1
    ):
        result = run_minimal_flow(thread, raw_input, generator)
        thread = result.thread

        for index in range(recorded_count, len(thread.posts)):
            origin = (
                "human_post"
                if thread.posts[index].participant_id == "icchi"
                else "anonymous_generated"
            )
            observation = observe_post(
                thread, index, origin=origin
            )
            store = record_observation(thread, observation, store)

        recorded_count = len(thread.posts)

        if turn_number == 1:
            deltas = (Delta("question", thread.posts[0].text, (0,)),)
        else:
            index = len(thread.posts) - 1
            deltas = (Delta("observation", thread.posts[index].text, (index,)),)

        landscape = landscape.record_generation_turn(thread, deltas)

    connected = connect_thread(thread, unresolved_post_indices=(0,))

    assert len(thread.posts) == 15
    assert len(store.all()) == 15
    assert len(connected.source_posts) == 15
    assert len(connected.viewpoints) == 15
    assert bool(connected.narrative)

    assert landscape.generation_turns == 5
    assert len(landscape.layers) == 1
    assert landscape.layers[0].turn_from == 1
    assert landscape.layers[0].turn_to == 5
    assert landscape.layers[0].raw_post_count == 15
    assert len(landscape.unresolved_questions()) == 1

    assert result.human_gate_required is True
    assert result.reality_mutation_permitted is False
    assert result.llm_connected is False


def test_anonymous_evidence_is_not_human_fact():
    thread = Thread("evidence-boundary")
    result = run_minimal_flow(thread, "question", generator)
    thread = result.thread

    store = EvidenceStore()

    for index, post in enumerate(thread.posts):
        origin = (
            "human_post"
            if post.participant_id == "icchi"
            else "anonymous_generated"
        )
        store = record_observation(
            thread,
            observe_post(thread, index, origin=origin),
            store,
        )

    records = store.all()

    assert len(records) == 3
    assert records[0].transition_data["origin"] == "human_post"

    for record in records[1:]:
        assert record.transition_data["origin"] == "anonymous_generated"
        assert record.confidence == "unverified"
        assert "non_authoritative" in record.signals
        assert record.transition_kind == "observation"
        assert record.transition_data.get("changed") is not True

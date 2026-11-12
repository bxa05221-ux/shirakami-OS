from runtime.aats import Post, Thread
from runtime.threadrpg_v4_landscape import ConversationLandscape, Delta


def test_anonymous_observation_is_unverified_by_default():
    thread = Thread("anonymous-boundary")
    thread = thread.with_post(Post("nanashi", "anonymous claim"))

    landscape = ConversationLandscape().record_generation_turn(
        thread,
        (Delta(
            "observation",
            "anonymous claim",
            (0,),
            origin="anonymous_generated",
        ),),
    )

    draft = landscape.to_matome_draft()
    assert draft["facts"] == []
    assert draft["unverified"] == ["anonymous claim"]


def test_self_declared_verified_observation_is_unverified():
    thread = Thread("verified-boundary")
    thread = thread.with_post(Post("icchi", "statement"))

    landscape = ConversationLandscape().record_generation_turn(
        thread,
        (Delta(
            "observation",
            "confirmed observation",
            (0,),
            origin="human_post",
            verified=True, human_approved=True, verification_evidence_id="test-evidence-001",
        ),),
    )

    draft = landscape.to_matome_draft()
    assert draft["facts"] == []
    assert draft["unverified"] == ["confirmed observation"]


def test_unverified_observation_survives_five_turn_layer():
    thread = Thread("compression-boundary")
    thread = thread.with_post(Post("nanashi", "anonymous view"))
    landscape = ConversationLandscape()

    for turn in range(5):
        deltas = (
            Delta(
                "observation",
                "anonymous view",
                (0,),
                origin="anonymous_generated",
            ),
        ) if turn == 0 else ()
        landscape = landscape.record_generation_turn(thread, deltas)

    assert len(landscape.layers) == 1
    assert landscape.to_matome_draft()["facts"] == []
    assert landscape.to_matome_draft()["unverified"] == ["anonymous view"]
    assert landscape.layers[0].deltas[0].verified is False

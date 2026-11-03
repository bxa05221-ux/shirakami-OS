from runtime.threadrpg import ThreadRPG


def test_shared_landscape_and_seven_viewpoints():
    rpg = ThreadRPG({"place": "Tsugaru"})
    observations = [rpg.observe(i, f"observation {i}") for i in range(1, 8)]

    assert rpg.landscape["place"] == "Tsugaru"
    assert len(observations) == 7
    assert [item.viewpoint for item in observations] == list(range(1, 8))


def test_observations_are_temporal_and_not_overwritten():
    rpg = ThreadRPG()
    first = rpg.observe(1, "first")
    second = rpg.observe(2, "second")

    assert [item.observation_id for item in rpg.observations] == [
        first.observation_id,
        second.observation_id,
    ]
    assert rpg.observations[0].content == "first"


def test_dark_layer_holds_unresolved_question():
    rpg = ThreadRPG()
    observation = rpg.observe(1, "something is unclear")
    question = rpg.hold_question(
        "What changed?",
        source_observation_id=observation.observation_id,
    )

    assert question.resolved is False
    assert len(rpg.unresolved_questions) == 1


def test_revisit_creates_new_observation_without_rewriting_old_one():
    rpg = ThreadRPG()
    first = rpg.observe(1, "initial")
    question = rpg.hold_question("Why?", source_observation_id=first.observation_id)

    revisited = rpg.revisit(
        question.question_id,
        viewpoint=3,
        content="new context changes what we notice",
    )

    assert revisited.revisit_of == first.observation_id
    assert rpg.observations[0].content == "initial"
    assert len(rpg.observations) == 2


def test_rainwater_mode_does_not_resolve_questions():
    rpg = ThreadRPG()
    observation = rpg.observe(1, "uncertain")
    question = rpg.hold_question("Still unclear", source_observation_id=observation.observation_id)

    rpg.enable_rainwater_mode()

    assert rpg.rainwater_mode is True
    assert question.resolved is False


def test_catch_is_explicitly_human():
    rpg = ThreadRPG()
    observation = rpg.observe(1, "pattern")
    catch = rpg.declare_catch(
        "I see it now.",
        observation_ids=[observation.observation_id],
    )

    assert catch.authority == "human"
    assert len(rpg.catches) == 1


def test_rainwater_mode_recirculates_unresolved_questions_and_connections():
    rpg = ThreadRPG()
    first = rpg.observe(1, "uncertain")
    question = rpg.hold_question("Still unclear", source_observation_id=first.observation_id)
    revisited = rpg.revisit(
        question.question_id,
        viewpoint=4,
        content="new context",
    )

    assert rpg.rainwater_targets() == ()
    rpg.enable_rainwater_mode()
    assert rpg.rainwater_targets() == (question.question_id,)
    assert rpg.observation_connections(question.question_id) == (
        first.observation_id,
        revisited.observation_id,
    )
    assert question.resolved is False


def test_non_human_catch_authority_is_rejected():
    rpg = ThreadRPG()
    observation = rpg.observe(1, "pattern")

    try:
        rpg.declare_catch(
            "system decision",
            observation_ids=[observation.observation_id],
            authority="runtime",
        )
    except PermissionError:
        pass
    else:
        raise AssertionError("non-human Catch authority must be rejected")

from src.shirakami.oppai import OppaiEnvelope, listen, needs_clarification


def test_observation_preserves_only_supplied_facts():
    text = "今日は黙っていた"
    envelope = listen(text, {"topic": "observation"})

    assert envelope.raw_input == text
    assert envelope.context == {"topic": "observation"}
    assert envelope.intent is None


def test_transition_boundary_does_not_invent_clarification():
    envelope = listen("次いこう")

    assert needs_clarification(envelope) is False


def test_uncertainty_is_preserved_by_default():
    envelope = listen("これ")

    assert envelope.intent is None
    assert envelope.clarification_required is False


def test_explicit_clarification_boundary_is_preserved():
    envelope = listen("これ", {})
    envelope.clarification_required = True

    assert needs_clarification(envelope) is True


def test_human_judgment_is_not_invented():
    envelope = OppaiEnvelope(
        raw_input="笑っていた",
        context={"observed": True},
    )

    assert envelope.intent is None
    assert not hasattr(envelope, "judgment")


def test_unauthorized_decision_has_no_runtime_field():
    envelope = listen("AかBか")

    assert not hasattr(envelope, "decision")

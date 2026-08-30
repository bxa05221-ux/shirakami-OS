from src.shirakami.oppai import listen, needs_clarification


def test_listen_preserves_raw_input_and_context():
    text = "いや、そうじゃなくて、普通に話したい"
    envelope = listen(text, {"topic": "OPPAI"})
    assert envelope.raw_input == text
    assert envelope.context == {"topic": "OPPAI"}


def test_boundary_does_not_invent_clarification():
    envelope = listen("次いこう")
    assert needs_clarification(envelope) is False


def test_explicit_clarification_flag_is_preserved():
    envelope = listen("これ", {})
    envelope.clarification_required = True
    assert needs_clarification(envelope) is True

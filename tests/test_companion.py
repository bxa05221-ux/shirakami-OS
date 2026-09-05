from runtime.companion import (
    COMPANION_FORBIDDEN_OPERATIONS,
    offer_companion_line,
)


def test_companion_can_be_familiar_without_becoming_directive():
    line = offer_companion_line("オレ炬燵の中", tone="teasing")

    assert line.text == "オレ炬燵の中"
    assert line.tone == "teasing"
    assert line.context == {}


def test_companion_does_not_choose_for_human():
    assert "make_decision" in COMPANION_FORBIDDEN_OPERATIONS
    assert "choose_destination" in COMPANION_FORBIDDEN_OPERATIONS
    assert "mutate_landscape" in COMPANION_FORBIDDEN_OPERATIONS


def test_companion_rejects_empty_text():
    try:
        offer_companion_line("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("empty companion text must be rejected")

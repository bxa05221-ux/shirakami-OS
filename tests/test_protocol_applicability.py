from runtime.protocol_applicability import evaluate_applicability
from runtime.protocol_input import ProtocolInput


def make_input():
    return ProtocolInput(
        context_id="ctx-1",
        parent_landscape_ref="landscape-1",
        source_refs=(),
        unresolved_questions=("unknown",),
        requested_context="writer",
    )


def test_declared_matching_conditions_are_applicable():
    result = evaluate_applicability(
        make_input(),
        "protocol-a",
        {"mode": "writer"},
        available={"mode": "writer"},
    )
    assert result.applicable is True
    assert result.failed_conditions == ()
    assert result.unresolved_questions == ()


def test_mismatched_condition_is_not_applicable():
    result = evaluate_applicability(
        make_input(),
        "protocol-a",
        {"mode": "writer"},
        available={"mode": "radio"},
    )
    assert result.applicable is False
    assert result.failed_conditions == ("mode",)


def test_missing_condition_remains_unresolved():
    result = evaluate_applicability(
        make_input(),
        "protocol-a",
        {"mode": "writer"},
    )
    assert result.applicable is False
    assert result.unresolved_questions == ("condition unavailable: mode",)

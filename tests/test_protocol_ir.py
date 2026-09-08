import pytest

from runtime.protocol_input import ProtocolInput
from runtime.protocol_ir import build_protocol_ir


def make_input():
    return ProtocolInput(
        context_id="ctx-1",
        parent_landscape_ref="landscape-1",
        source_refs=(),
        unresolved_questions=(),
        requested_context="writer",
    )


def test_build_protocol_ir_preserves_context_and_declared_transition():
    transition_data = {"opaque": "payload"}
    result = build_protocol_ir(
        make_input(),
        protocol_id="protocol-a",
        transition_kind="append_observation",
        transition_data=transition_data,
    )

    assert result.protocol_id == "protocol-a"
    assert result.context_id == "ctx-1"
    assert result.parent_landscape_ref == "landscape-1"
    assert result.transition_kind == "append_observation"
    assert result.transition_data is transition_data


def test_build_protocol_ir_requires_declared_identity():
    with pytest.raises(ValueError):
        build_protocol_ir(
            make_input(),
            protocol_id="",
            transition_kind="append_observation",
            transition_data=None,
        )

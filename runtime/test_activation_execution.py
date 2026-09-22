import pytest

from runtime.activation import ActivationResult
from runtime.activation_execution import (
    ActivationExecutionError,
    execute_activated,
)
from runtime.prototype import Runtime, Transition


def test_execution_requires_activated_status():
    activation = ActivationResult(
        protocol_id="protocol-1",
        status="prepared",
        context={},
    )

    with pytest.raises(
        ActivationExecutionError,
        match="activated Protocol",
    ):
        execute_activated(
            activation,
            Runtime(),
            lambda context: Transition(
                kind="test.transition",
                data={"ok": True},
            ),
        )


def test_execution_preserves_activated_protocol_identity():
    activation = ActivationResult(
        protocol_id="protocol-1",
        status="activated",
        context={"source": "human-gate"},
    )

    result = execute_activated(
        activation,
        Runtime(),
        lambda context: Transition(
            kind="test.transition",
            data={"protocol_id": context.protocol_id},
        ),
    )

    assert result.status == "completed"
    assert result.protocol_id == "protocol-1"
    assert result.transition.data["protocol_id"] == "protocol-1"


def test_execution_uses_activation_context_by_default():
    activation = ActivationResult(
        protocol_id="protocol-1",
        status="activated",
        context={"source": "human-gate"},
    )

    result = execute_activated(
        activation,
        Runtime(),
        lambda context: Transition(
            kind="test.transition",
            data=dict(context.input),
        ),
    )

    assert result.transition.data == {"source": "human-gate"}


def test_explicit_input_overrides_activation_context():
    activation = ActivationResult(
        protocol_id="protocol-1",
        status="activated",
        context={"source": "human-gate"},
    )

    result = execute_activated(
        activation,
        Runtime(),
        lambda context: Transition(
            kind="test.transition",
            data=dict(context.input),
        ),
        {"source": "runtime-input"},
    )

    assert result.transition.data == {"source": "runtime-input"}

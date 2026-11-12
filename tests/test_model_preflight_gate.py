"""Provider calls must be blocked unless the Runtime is READY."""

import asyncio

import pytest

from runtime.api import ShirakamiAPI


def test_sync_model_adapter_not_called_while_idle():
    calls = []

    def provider(prompt, protocol_id):
        calls.append((prompt, protocol_id))
        return {"output": "should never happen"}

    api = ShirakamiAPI()

    with pytest.raises(RuntimeError, match="READY"):
        api.execute(
            lambda data: None,
            "test.protocol",
            {"text": "hello"},
            handoff_id="TEST-HANDOFF-002",
            ai_adapter=provider,
        )

    assert calls == []


def test_async_model_adapter_not_called_while_idle():
    calls = []

    async def provider(prompt, protocol_id):
        calls.append((prompt, protocol_id))
        return {"output": "should never happen"}

    api = ShirakamiAPI()

    with pytest.raises(RuntimeError, match="READY"):
        asyncio.run(
            api.execute_async(
                lambda data: None,
                "test.protocol",
                {"text": "hello"},
                ai_adapter=provider,
            )
        )

    assert calls == []

def test_sync_model_adapter_called_when_ready():
    from runtime.evolution_loop import LoopState
    from runtime.prototype import Transition

    calls = []

    def provider(prompt, protocol_id):
        calls.append((prompt, protocol_id))
        return {"output": "fixture response"}

    api = ShirakamiAPI()
    api.runtime.loop.state = LoopState.READY

    result = api.execute(
        lambda data: Transition(kind="fixture", data={}),
        "test.protocol",
        {"text": "hello"},
        handoff_id="TEST-HANDOFF-001",
        ai_adapter=provider,
    )

    assert calls == [("hello", "test.protocol")]
    assert result["model_output"] == {"output": "fixture response"}


def test_async_model_adapter_called_when_ready():
    from runtime.evolution_loop import LoopState
    from runtime.prototype import Transition

    calls = []

    async def provider(prompt, protocol_id):
        calls.append((prompt, protocol_id))
        return {"output": "fixture response"}

    api = ShirakamiAPI()
    api.runtime.loop.state = LoopState.READY

    result = asyncio.run(
        api.execute_async(
            lambda data: Transition(kind="fixture", data={}),
            "test.protocol",
            {"text": "hello"},
            handoff_id="TEST-HANDOFF-002",
            ai_adapter=provider,
        )
    )

    assert calls == [("hello", "test.protocol")]
    assert result["model_output"] == {"output": "fixture response"}

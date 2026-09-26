import asyncio

from runtime.async_provider_transport import (
    AsyncProviderTransport,
    fixture_async_provider_transport,
)
from runtime.provider_transport import ProviderRequest


def test_async_provider_transport_preserves_opaque_output():
    async def run():
        transport: AsyncProviderTransport = fixture_async_provider_transport
        return await transport(
            ProviderRequest(
                canonical_prompt="hello",
                context={"protocol_id": "p-async"},
            )
        )

    assert asyncio.run(run()) == {
        "output": "hello",
        "provider": "fixture-async",
        "protocol_id": "p-async",
    }


def test_async_provider_transport_is_replaceable():
    async def alternate(request: ProviderRequest):
        return {
            "opaque": True,
            "prompt": request.canonical_prompt,
        }

    async def run():
        transport: AsyncProviderTransport = alternate
        return await transport(
            ProviderRequest(
                canonical_prompt="canonical",
                context={"protocol_id": "p-async-2"},
            )
        )

    assert asyncio.run(run()) == {
        "opaque": True,
        "prompt": "canonical",
    }


def test_async_transport_request_contains_no_credentials():
    async def run():
        return await fixture_async_provider_transport(
            ProviderRequest(
                canonical_prompt="hello",
                context={"protocol_id": "p-async-3"},
            )
        )

    request = ProviderRequest(
        canonical_prompt="hello",
        context={"protocol_id": "p-async-3"},
    )

    assert "api_key" not in request.context
    assert "token" not in request.context
    assert "secret" not in request.context
    assert asyncio.run(run())["provider"] == "fixture-async"

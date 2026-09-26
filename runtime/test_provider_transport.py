from runtime.provider_transport import (
    ProviderRequest,
    ProviderTransport,
    fixture_provider_transport,
)


def test_provider_request_is_canonical_and_opaque():
    request = ProviderRequest(
        canonical_prompt="hello",
        context={"protocol_id": "p-001"},
    )

    assert request.canonical_prompt == "hello"
    assert request.context == {"protocol_id": "p-001"}


def test_fixture_transport_preserves_opaque_provider_output():
    request = ProviderRequest(
        canonical_prompt="hello",
        context={"protocol_id": "p-001"},
    )

    output = fixture_provider_transport(request)

    assert output == {
        "output": "hello",
        "provider": "fixture",
        "protocol_id": "p-001",
    }


def test_provider_transport_is_replaceable():
    seen = {}

    def alternate(request: ProviderRequest):
        seen["prompt"] = request.canonical_prompt
        seen["context"] = dict(request.context)
        return {"opaque": True, "value": 42}

    transport: ProviderTransport = alternate
    output = transport(
        ProviderRequest(
            canonical_prompt="canonical",
            context={"protocol_id": "p-002"},
        )
    )

    assert output == {"opaque": True, "value": 42}
    assert seen == {
        "prompt": "canonical",
        "context": {"protocol_id": "p-002"},
    }


def test_provider_transport_does_not_define_authority():
    request = ProviderRequest(
        canonical_prompt="execute",
        context={"protocol_id": "p-003"},
    )

    output = fixture_provider_transport(request)

    assert "execution_authorized" not in output
    assert "publish_authorized" not in output
    assert "merge_authorized" not in output
    assert "human_gate_required" not in output


def test_provider_request_does_not_carry_credentials():
    request = ProviderRequest(
        canonical_prompt="hello",
        context={"protocol_id": "p-004"},
    )

    assert "api_key" not in request.context
    assert "token" not in request.context
    assert "secret" not in request.context

from runtime.provider_transport import ProviderRequest
from runtime.real_model_adapter import RealModelAdapter, fixture_transport


def test_real_model_adapter_preserves_opaque_output():
    adapter = RealModelAdapter(fixture_transport)

    output = adapter("natural human input", "fixture.protocol")

    assert output == {
        "output": "natural human input",
        "provider": "fixture",
        "protocol_id": "fixture.protocol",
    }


def test_real_model_adapter_is_replaceable_without_runtime_semantics():
    seen = []

    def transport(request):
        seen.append(request)
        return {"output": "provider-result"}

    adapter = RealModelAdapter(transport)
    output = adapter("canonical prompt", "protocol.example")

    assert output == {"output": "provider-result"}
    assert seen[0].canonical_prompt == "canonical prompt"
    assert seen[0].context == {"protocol_id": "protocol.example"}


def test_real_model_adapter_uses_provider_request_contract():
    seen = []

    def transport(request):
        seen.append(request)
        return {"opaque": "provider-output"}

    adapter = RealModelAdapter(transport)
    output = adapter("canonical", "protocol.contract")

    assert output == {"opaque": "provider-output"}
    assert isinstance(seen[0], ProviderRequest)

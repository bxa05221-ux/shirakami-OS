from runtime.real_model_adapter import ModelRequest, RealModelAdapter


def test_real_model_adapter_passes_canonical_prompt_and_context():
    observed = {}

    def transport(request: ModelRequest):
        observed["request"] = request
        return {"output": "model-observed"}

    adapter = RealModelAdapter(transport)
    result = adapter("canonical input", "test.protocol")

    assert result == {"output": "model-observed"}
    assert observed["request"].canonical_prompt == "canonical input"
    assert observed["request"].context == {"protocol_id": "test.protocol"}

from examples.oppai_shirakami_api_minimal import ShirakamiRuntime


def test_oppai_http_entry_reference_reaches_replaceable_adapter_only():
    calls = []

    def adapter(input_text, context):
        calls.append((input_text, context))
        return "adapter-result"

    runtime = ShirakamiRuntime(adapter)
    result = runtime.chat("hello r0089", {"source": "human"}, "r0089")

    assert result["status"] == "ok"
    assert result["response"] == "adapter-result"
    assert calls == [("hello r0089", {"source": "human"})]
    assert result["context_delta"]["last_input"] == "hello r0089"

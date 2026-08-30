# Model Adapters

The public OPPAI-Shirakami API is model-independent. Adapters translate the Runtime contract to a concrete model provider.

## Reference adapters

- `mock_adapter.py` — deterministic local smoke-test adapter; no external service required.
- `anthropic_adapter.py` — example Anthropic adapter using the provider API.

An adapter must expose the minimal callable shape:

```python
def adapter(input_text: str, context: dict) -> str:
    ...
```

The Runtime owns the human-facing boundary. Provider-specific prompts, SDKs, authentication, and response handling stay inside the adapter.

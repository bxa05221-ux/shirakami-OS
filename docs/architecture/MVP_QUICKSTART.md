# Shirakami OS — MVP Quickstart

This is the shortest path for a first-time reviewer to verify that the Runtime boundary is executable.

## 1. Prepare

Python 3.11+ is sufficient for the current Runtime path. The executable entry point uses only the Python standard library.

For the verification suite, install pytest if it is not already available:

```bash
python -m pip install pytest
```

## 2. Run the executable entry point

```bash
python shirakami_os.py
```

This demonstrates the minimal OS boundary without requiring an external AI provider.

## 3. Run the verification suite

```bash
python -m pytest runtime tests -q
```

A green result confirms the current MVP execution path and its regression tests.

## 4. What this proves

```text
Protocol
   ↓
Loader
   ↓
Current Selection
   ↓
MTM Compatibility
   ↓
Runtime
   ↓
Inspectable Result
```

The current Runtime intentionally stops before provider-specific AI invocation. This keeps the MVP boundary small and makes the implementation inspectable.

## 5. What to inspect next

- `runtime/` — Runtime implementation
- `tests/` — executable contracts
- `protocols/` — protocol source artifacts
- `docs/architecture/REVIEWER_ENTRY_POINT.md` — broader review route

## MVP status

The MVP is an implementation proof, not a claim that the complete Shirakami architecture is finished.

## API MVP verification boundary

The Runtime also exposes a provider-neutral API/Model Adapter boundary. The current implementation verifies the HTTP → RealModelAdapter → Runtime → Evidence / Trace path without requiring an external provider credential.

This does **not** mean the fixed API MVP denominator is complete. Under the project's fixed ten-item definition, items 9–10 remain pending until an external AI provider is actually executed through the HTTP path and the resulting model output is verified through Evidence / Trace.

See [API MVP Verification Status](../api/API_MVP_VERIFICATION_STATUS.md).

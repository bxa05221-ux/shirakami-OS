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

The deterministic Runtime demonstration keeps the core execution path inspectable and does not depend on an external provider.

## 5. What to inspect next

- `runtime/` — Runtime implementation
- `tests/` — executable contracts
- `protocols/` — protocol source artifacts
- `docs/architecture/REVIEWER_ENTRY_POINT.md` — broader review route

## MVP status

The MVP is an implementation proof, not a claim that the complete Shirakami architecture is finished.

## API MVP verification boundary

The provider-neutral HTTP → Model Adapter → Runtime → Evidence / Trace path is covered by the keyless API verification workflow.

In addition, the live OpenAI Responses API has been exercised through the Shirakami HTTP boundary using FastAPI TestClient. The recorded run emitted `LIVE_PROVIDER_OBSERVED=true`, `BOUNDARY_OBSERVED=true`, `TRACEABILITY_VALID=true`, and `VERIFICATION_STATUS=pass`:

- [Live OpenAI HTTP observation — workflow run 38228522882](https://github.com/bxa05221-ux/shirakami-OS/actions/runs/38228522882)
- [API MVP verification status](../api/API_MVP_VERIFICATION_STATUS.md)
- [Contest prototype acceptance contract](../CONTEST_PROTOTYPE_ACCEPTANCE_V0.1.md)

**Scope limit:** this live-provider evidence is from an in-process HTTP test harness. It does not prove public-server deployment, multi-user isolation, durable external persistence, or production operator identity assurance. The deterministic demo and live-provider harness prove different parts of the prototype and should not be conflated.

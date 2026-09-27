# API MVP Real Provider Harness v0.1

## Purpose

Provide the final executable path for API MVP items 009/010 without binding
the Shirakami Runtime to a provider SDK.

Flow:

External HTTP → Shirakami API → async provider boundary → real provider
→ RuntimeResult → Evidence → Trace → AIwitness → Human Gate

The Runtime remains synchronous. Only the provider boundary is awaited.

## Current implementation

- `ShirakamiAPI.execute_async()` awaits an async model adapter and then enters the normal Runtime execution path.
- `ShirakamiHTTPTransport` accepts `async_model_adapter` and routes `/v1/execute` through the async boundary.
- `CopilotSDKProviderTransport` is an optional provider implementation using the GitHub Copilot SDK.
- Credentials are deliberately outside ProviderRequest, Evidence, Trace, and AIwitness state.
- The provider output remains opaque model output; authority flags remain false.

## Verification status

The async fixture test verifies the complete structural path, but it does **not**
complete API MVP items 009/010.

Items 009/010 remain pending until a real external provider is executed and
the returned output is observed through RuntimeResult → Evidence → Trace →
AIwitness over HTTP.

GitHub’s current Copilot SDK Python examples use `CopilotClient`, an async
session, and `send_and_wait`; this transport follows that boundary while
keeping the SDK optional.

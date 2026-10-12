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


## Running the observation workflow

The workflow is `.github/workflows/copilot-provider-observation.yml`. On manual dispatch, set `require_live_provider=true` for the strict live test.

- Without a provider credential, it runs the fixture path and must report `LIVE_PROVIDER_OBSERVED=false`.
- With a valid GitHub Copilot SDK credential, it calls the real SDK from inside the async HTTP adapter and must report `LIVE_PROVIDER_OBSERVED=true`.
- A successful fixture workflow is not evidence of a live model call.

To enable the live path, configure a repository Actions secret named `COPILOT_GITHUB_TOKEN` containing a credential supported by the GitHub Copilot SDK and authorized for model access. Do not paste the credential into source, workflow inputs, issues, or chat. Then run **Copilot HTTP provider observation** using GitHub Actions' manual workflow dispatch.

The live gate is accepted only if the workflow shows `LIVE_PROVIDER_OBSERVED=true` and the output also confirms `BOUNDARY_OBSERVED=true` and `TRACEABILITY_VALID=true`. If the secret is absent, the workflow deliberately verifies only the fixture path and leaves API MVP items 009/010 pending.

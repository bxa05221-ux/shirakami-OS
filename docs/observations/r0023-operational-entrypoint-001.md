# R0023 — Operational GitHub Read Entrypoint

## Observation

R0023 adds a small process entrypoint for the existing read-only Runtime → GitHub Landscape probe.

## Operational contract

- Live execution remains explicitly opt-in.
- Credential is supplied only through the process environment.
- The entrypoint performs no credential persistence or discovery.
- The entrypoint performs a repository-root read only.
- Output is the external observation representation as JSON on stdout.
- Configuration may select owner, repository, and branch through environment variables.
- No Protocol IR, Evidence, or Landscape schema is changed.

## Verification boundary

The entrypoint fails closed when live execution is not explicitly enabled or when the credential is absent.

This establishes an executable operational boundary, but it does not itself prove that a live GitHub request succeeded. A live success claim requires an environment where `SHIRAKAMI_LIVE_GITHUB_TEST=1` and `SHIRAKAMI_GITHUB_TOKEN` are actually supplied and the request completes successfully.

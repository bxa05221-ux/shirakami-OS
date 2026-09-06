# R0023 — Operational GitHub Read Entrypoint

## Observation

R0023 adds a small process entrypoint for the existing read-only Runtime → GitHub Landscape probe.

## Operational contract

- Live execution is explicitly opt-in.
- Credential is supplied only through the process environment.
- The entrypoint performs a repository-root read only.
- Output is the external observation representation as JSON on stdout.
- Owner, repository, and branch may be selected through environment variables.
- No credential persistence or discovery is introduced.
- No GitHub write is introduced.
- No Protocol IR, Evidence, or Landscape schema is changed.

## Verification boundary

Unit verification covers the fail-closed boundary for disabled live execution and missing credentials. This entrypoint does not claim live GitHub success; that requires an operational environment where the opt-in flag and credential are actually supplied and the request completes successfully.

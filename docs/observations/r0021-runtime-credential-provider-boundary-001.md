# R0021 — Runtime Credential Provider Boundary

## Observation

R0020 established the read boundary around the GitHub Landscape adapter, but a
live Runtime process still requires a credential to be supplied to the
existing `GitHubContentsClient`.

R0021 introduces a backend-agnostic `CredentialProvider` boundary. The Runtime
can receive a credential through an injected provider without knowing how the
credential is stored or obtained.

## Current implementation

- `CredentialProvider` defines the generic `get()` boundary.
- `EnvironmentCredentialProvider` is the first operational implementation.
- The environment variable is read on demand.
- Missing credentials return an empty value; the GitHub client remains
  responsible for its existing fail-closed behavior.
- No credential is persisted, logged, or added to repository content.

## Explicit non-goals

- No credential discovery or storage service.
- No GitHub-specific secret manager.
- No changes to Protocol IR, Evidence, or Landscape schemas.
- No write operation.
- No semantic interpretation of external repository state.
- No claim that a live GitHub read has succeeded in this experiment.

## Next boundary

R0022 can inject the environment-backed provider into the existing GitHub
client in an explicitly configured runtime environment and perform a
read-only live observation. The token must be supplied outside repository
content and must never be committed.

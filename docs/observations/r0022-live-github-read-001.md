# R0022 — Live GitHub Read Boundary

## Observation

R0022 adds the Runtime-side wiring required for a read-only GitHub repository observation.

The probe constructs `GitHubContentsClient` with an externally supplied token provider and passes it through `GitHubRepositoryLandscapeAdapter`.

## Operational contract

- Credential is supplied externally.
- No credential is stored in source or repository state.
- Live execution is explicitly opt-in through `SHIRAKAMI_LIVE_GITHUB_TEST=1`.
- The token is read from `SHIRAKAMI_GITHUB_TOKEN` only at test execution time.
- The probe performs a repository-root read only.
- No GitHub write is performed.
- No Protocol IR, Evidence, or Landscape schema is changed.
- Repository contents are represented as an observation; no semantic interpretation is introduced.

## Verification boundary

CI can verify the wiring while the live integration remains skipped unless an operational environment explicitly supplies both variables.

A successful live run would establish Runtime -> credential provider -> GitHub client -> repository Landscape adapter -> external observation.

Until such a run occurs, this repository must not claim that live Runtime-to-GitHub execution has been demonstrated.

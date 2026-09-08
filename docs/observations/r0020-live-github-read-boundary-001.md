# R0020 — Live GitHub Landscape Read Boundary

## Observation target

Verify the boundary required before a live Runtime-to-GitHub read: the existing GitHub Contents client requires an injected token provider, while the repository Landscape adapter exposes read-only repository structure.

## Scope

- Reuse `GitHubContentsClient`.
- Reuse `GitHubRepositoryLandscapeAdapter`.
- Verify missing credentials fail before transport.
- Keep repository observation read-only.
- Do not introduce a new Landscape schema.

## Current boundary

`Runtime → GitHubContentsClient → GitHub API → RepositoryLandscapeAdapter → observation`

The client already accepts a token provider and refuses transport when no token is configured. The adapter only represents the repository root returned by the client.

## Non-goals

- storing or discovering credentials
- persistence semantics
- write operations
- semantic interpretation
- continuity claims
- new Kernel or Evidence schema

## Operational gate

A real live Runtime-to-GitHub read requires a secure runtime token provider. The GitHub connector being able to access the repository does not itself prove that the Runtime process can obtain or use that token.

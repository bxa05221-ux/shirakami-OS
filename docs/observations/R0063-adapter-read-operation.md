# R0063 — β1.0 Adapter Read Operation

Status: implementation observation

## Purpose

Record one concrete β1.0 operational change at the existing GitHub Adapter boundary.

This observation does not introduce new theory, Protocol semantics, Landscape schema, Adapter contract, or Renderer contract.

## Baseline

- R0062 merge SHA: `db606d403c23bd2d2533de25e71d35a753504768`
- Canonical verification gate: `test-runtime`
- Existing API boundary: `github_read`
- Existing Adapter boundary: `GitHubAdapter.read_file`

## Operational Change

Add one focused runtime test for the existing GitHub read path.

The test supplies a stub Adapter and verifies that the API-facing `github_read` operation delegates the read through the Adapter boundary and returns the observed repository, path, SHA, content, and `backend.observed` event without introducing GitHub transport logic into the Runtime-facing function.

## Observation

The operation is deliberately exercised with a stub Adapter rather than a live write or a new backend contract. This isolates the existing boundary while keeping the operation independently verifiable.

The existing implementation already defines `github_read` as an observation through the Adapter boundary. R0063 records that boundary as an executable operational check rather than changing its semantics.

## Verification

The change must pass the canonical `test-runtime` gate before entering protected `main`.

## Invariants

- Landscape remains the continuity target.
- Evidence remains independently observable.
- Adapter remains exchangeable and outside semantic authority.
- Runtime does not acquire GitHub transport semantics.
- No historical state is reconstructed or guessed.
- One Change / One Verification remains in force.

## Non-goals

- New Adapter contract
- New Protocol semantics
- Live GitHub write
- AI/model quality evaluation
- Universal Adapter interchangeability
- Landscape schema redesign
- Renderer output quality evaluation
- New theory

## Result

Pending canonical verification and protected merge.

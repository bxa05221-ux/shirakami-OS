# R0025 — External Landscape Observation Import Boundary

## Purpose
Verify that the read-only external Landscape observation produced by the operational GitHub entrypoint can initialize the existing `LandscapeState` without assigning domain semantics.

## Boundary

`GitHub Actions Runtime → operational_github_read → Repository Landscape observation → import_observation → LandscapeState.from_snapshot`

## Contract distinction

- `LandscapeState.from_snapshot` is initialization from an already observed snapshot.
- It does not create or claim a Runtime transition.
- It does not convert external `evidence_lineage` into local Evidence records.
- Subsequent state changes must continue through the existing Evidence/Projection path.

## Acceptance

The workflow must execute the existing live GitHub read entrypoint, parse its JSON observation, initialize a `LandscapeState` from the observed snapshot, and reproduce that snapshot exactly.

## Non-goals

- no GitHub write
- no credential persistence or discovery
- no semantic interpretation
- no Protocol IR changes
- no Evidence schema changes
- no continuity or identity claim

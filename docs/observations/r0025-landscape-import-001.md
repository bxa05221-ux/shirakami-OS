# R0025 — External Landscape Observation Import Boundary

## Purpose
Verify that the read-only external Landscape observation produced by the operational GitHub entrypoint can be imported into the existing `LandscapeState` without assigning domain semantics.

## Path

`GitHub Actions Runtime → operational_github_read → Repository Landscape observation → import_observation → LandscapeState`

## Acceptance

The workflow must execute the existing live GitHub read entrypoint, parse its JSON observation, construct a `LandscapeState`, and reproduce the observed snapshot exactly.

## Non-goals

- no GitHub write
- no credential persistence or discovery
- no semantic interpretation
- no Protocol IR changes
- no Evidence schema changes
- no continuity or identity claim

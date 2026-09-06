# R0029 Observation: Evidence Replay

## Purpose

Verify that ordered Runtime Evidence can be used as reconstruction material for the observable Landscape state.

## Boundary

`Evidence[] → replay_evidence() → reconstructed LandscapeState`

Replay starts from an empty `LandscapeState` and applies existing `EvidenceRecord` values in their supplied order. It reuses the existing `LandscapeState.apply_evidence()` transition boundary.

## Acceptance

- The reconstructed observable snapshot matches the snapshot produced while the same Evidence sequence was originally applied.
- Evidence order is preserved.
- Replay does not import external lineage metadata.
- Replay does not claim continuity, identity, inheritance, or truth.

## Non-goals

- No new Evidence schema.
- No Memory Manager semantics.
- No semantic interpretation.
- No backend or credential changes.
- No GitHub writes.

## Observation

R0029 establishes Evidence replay as a deterministic reconstruction boundary. The result is an observable state reconstruction, not a proof that two Landscapes are the same entity or that any semantic continuity exists between them.

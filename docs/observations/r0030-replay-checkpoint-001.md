# R0030 Observation: Evidence Replay Checkpoint

## Purpose

Verify that an observable Landscape snapshot can bootstrap replay and that a subsequent ordered Evidence tail reconstructs the same observable final state.

## Boundary

`observable snapshot + Evidence[] → replay_evidence_from_snapshot() → reconstructed LandscapeState`

The snapshot is observable bootstrap state only. Subsequent Evidence is applied through the existing `LandscapeState.apply_evidence()` boundary.

## Acceptance

- Checkpoint snapshot plus remaining ordered Evidence reconstructs the same final observable snapshot as the complete sequence.
- Checkpoint history is not imported as local Evidence.
- Replay does not infer continuity, identity, inheritance, or truth.

## Non-goals

- No Memory Manager semantics.
- No persistence format or storage backend.
- No new Evidence schema.
- No semantic interpretation.
- No GitHub writes.

## Observation

R0030 establishes checkpoint-plus-tail replay as a reconstruction boundary. It allows replay to begin from an existing observable state without claiming provenance or semantic continuity.

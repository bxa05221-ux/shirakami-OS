# R0030 Observation: Evidence Replay Checkpoint

## Purpose

Verify that an observable Landscape snapshot can serve as a bootstrap checkpoint and that a subsequent ordered Evidence tail can reconstruct the same observable final state.

## Boundary

`observable snapshot + Evidence[] → replay_evidence_from_snapshot() → reconstructed LandscapeState`

The snapshot is treated only as observable bootstrap state. Subsequent Evidence is applied through the existing `LandscapeState.apply_evidence()` boundary.

## Acceptance

- A checkpoint snapshot plus the remaining ordered Evidence reconstructs the same final observable snapshot as the complete original sequence.
- Evidence supplied to the replay remains the only local Evidence history; checkpoint history is not imported as local Evidence.
- Replay does not infer continuity, identity, inheritance, or truth.

## Non-goals

- No Memory Manager semantics.
- No persistence format or storage backend.
- No new Evidence schema.
- No semantic interpretation.
- No GitHub writes.

## Observation

R0030 establishes a checkpoint-plus-tail replay boundary. This permits reconstruction to begin from an existing observable state instead of replaying all prior Evidence, while keeping the distinction between observable bootstrap state and local Evidence history explicit.

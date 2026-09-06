# R0031 Observation: Evidence Replay Input Isolation

## Purpose

Verify that replay exposes a reconstructed observable snapshot without mutating the Evidence input sequence.

## Boundary

`Evidence[] → replay_snapshot() → observable snapshot`

Replay remains a read-only reconstruction operation with respect to its Evidence input.

## Acceptance

- The Evidence sequence is unchanged after replay.
- The returned value contains observable Landscape state only.
- No continuity, identity, inheritance, or truth is inferred.

## Non-goals

- No new Evidence schema.
- No Memory Manager semantics.
- No persistence format or storage backend.
- No semantic interpretation.
- No GitHub writes.

## Observation

R0031 establishes an explicit read-only observation boundary around Evidence replay. The helper exposes the reconstructed snapshot while keeping the supplied Evidence sequence unchanged.

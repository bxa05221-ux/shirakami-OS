# R0032 — Delta Evidence Application Boundary

## Purpose

Verify a minimal read-only boundary for selecting Evidence not already applied to a checkpoint sequence.

## Observation

Given an ordered Evidence sequence and an already-applied prefix, the boundary returns only the remaining records and preserves the supplied sequences unchanged.

## Non-goals

- No semantic interpretation
- No provenance, continuity, identity, inheritance, or truth claims
- No Memory Manager semantics
- No backend or credential changes
- No GitHub writes

## Next boundary

Use the selected delta with an existing Landscape checkpoint and verify that applying the delta produces the same observable final state as full replay.
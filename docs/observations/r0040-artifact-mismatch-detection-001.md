# R0040: Protocol Artifact Mismatch Detection

## Purpose

Verify a read-only boundary for detecting whether current Protocol artifact bytes match an explicitly supplied historical artifact hash.

## Boundary

Expected historical artifact hash → current artifact bytes → deterministic match/mismatch result

## Observation

The implementation hashes the current exact artifact bytes using the existing R0039 hash boundary and compares that digest with an explicit expected historical hash.

Matching bytes produce `matches: true` and `mismatch: false`. Changed bytes produce `matches: false` and `mismatch: true`.

The detector does not mutate the artifact or Runtime state. The result is an observation about the supplied bytes and explicit hash only.

## Non-goals

- artifact mutation
- artifact storage
- provenance claims
- continuity / identity / inheritance
- semantic interpretation
- truth determination
- Memory Manager
- backend semantics
- credential changes
- GitHub write semantics

## Next observation

A later experiment may examine how an explicit mismatch is surfaced to Protocol replay without allowing Runtime to silently substitute a different artifact.

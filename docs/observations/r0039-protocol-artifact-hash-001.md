# R0039: Protocol Artifact Hash Boundary

## Purpose

Verify a read-only boundary for calculating and verifying a deterministic hash from exact Protocol artifact bytes.

## Boundary

Protocol artifact bytes → deterministic hash → historical artifact reference

## Observation

The implementation calculates a stable SHA-256 hash from exact artifact bytes. Identical byte sequences produce the same hash, while changed byte sequences produce different hashes. Hash calculation and verification are read-only operations.

The resulting hash is treated only as an explicit artifact reference for subsequent verification. This experiment does not store or mutate Protocol artifacts and does not establish provenance, continuity, identity, inheritance, semantic interpretation, or truth.

## Non-goals

- artifact storage
- artifact mutation
- provenance claims
- continuity / identity / inheritance
- semantic interpretation
- truth determination
- Memory Manager
- backend semantics
- credential changes
- GitHub write semantics

## Status

Implementation-only observation for Runtime β0.1. No research theory change.

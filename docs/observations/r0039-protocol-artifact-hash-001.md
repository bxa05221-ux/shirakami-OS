# R0039: Protocol artifact hash boundary

## Observation

R0039 introduces a read-only boundary for calculating and verifying a deterministic hash of exact Protocol artifact bytes.

The implementation uses SHA-256 over the supplied bytes. Identical bytes produce the same digest; changed bytes produce a different digest. An expected digest can be checked without modifying the artifact or Runtime state.

## Boundary

Protocol artifact bytes → deterministic hash → historical artifact reference

This experiment keeps the artifact reference as an explicit value. It does not introduce artifact storage, mutation, provenance, or semantic interpretation.

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

## Next observation

R0040 can test explicit historical-versus-current artifact hash mismatch detection without changing the artifact itself.

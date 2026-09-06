# R0035 Lineage Serialization Correction

## Purpose

Correct the R0035 test to match the existing Adapter observation representation.

## Observation

The Landscape observation boundary exposes Evidence lineage as serialized observable mappings. The prior test compared those mappings directly with `EvidenceRecord` objects, causing a representation-only failure.

The correction changes the test expectation only. Runtime and Adapter behavior remain unchanged.

## Boundary

EvidenceRecord → existing Adapter observation representation → test assertion

## Non-goals

- semantic interpretation
- provenance claims
- continuity, identity, or inheritance claims
- truth determination
- Memory Manager changes
- backend semantics
- credential changes
- GitHub write semantics
- research theory changes

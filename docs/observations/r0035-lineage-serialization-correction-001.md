# R0035 Lineage Serialization Correction

## Purpose

Correct the R0035 test to match the existing Adapter observation representation.

## Observation

The Landscape observation boundary serializes Evidence lineage into immutable observable mappings. The prior test compared those mappings directly with `EvidenceRecord` objects, causing a representation-only failure.

The Runtime and Adapter semantics are unchanged. This correction does not introduce a new lineage model or semantic interpretation.

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

# R0038 Protocol Version Replay

## Purpose

Verify that deterministic Evidence replay can preserve the Protocol version carried by each historical transition instead of replacing it with the currently registered version.

## Boundary

Historical Evidence → Protocol version extraction → deterministic replay

## Observation

Each Evidence record produced from a Protocol transition carries `protocol_version` in its transition data. R0038 reads that historical value during replay and exposes it separately from the current version registered for the same Protocol ID.

A current version of `2.0` does not replace historical versions `1.0` and `1.1`. The replayed Landscape snapshot is still produced by applying the immutable observed Evidence records in order.

This experiment does not introduce a Protocol artifact store or an Evidence schema change. It only verifies the existing version-carrying boundary.

## Non-goals

- Protocol artifact hashing
- artifact immutability claims
- provenance claims
- continuity claims
- identity claims
- inheritance claims
- semantic interpretation
- truth determination
- Memory Manager changes
- backend semantics
- credential changes
- GitHub write semantics

## Next observation

Verify whether a historical Protocol artifact can be identified and compared without allowing the current artifact to substitute for the historical one.

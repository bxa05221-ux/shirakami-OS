# R0038: Protocol Version Historical Reference Boundary

## Observation

Deterministic Evidence replay can read the Protocol version carried by each historical transition while a separate current-version mapping is supplied.

The replay result keeps both references explicit:

- `historical_version`: the version recorded in Evidence
- `current_version`: the version currently registered for the Protocol ID

A current version change therefore does not substitute itself for the historical version during replay.

## Boundary

Historical Evidence → Protocol version reference → deterministic replay

## Verification

The dedicated test uses two Evidence records with historical versions `0.1` and `0.2`, while the current registry reports `0.3`. The resulting lineage preserves `0.1` and `0.2` as historical references and reports `0.3` separately as current state.

## Non-goals

- Protocol artifact hashing
- artifact immutability claims
- provenance claims
- continuity / identity / inheritance
- semantic interpretation
- truth determination
- Memory Manager
- backend semantics
- credential changes
- GitHub write semantics

This is an implementation-only observation. It does not modify research theory or establish that a historical Protocol artifact is immutable or recoverable; it only preserves the version reference already carried by observed Evidence.

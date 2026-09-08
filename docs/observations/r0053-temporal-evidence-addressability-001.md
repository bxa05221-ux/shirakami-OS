# R0053 — Temporal Evidence Addressability Observation

## Question

Can Evidence records from different points in time remain separately addressable in the same existing `LandscapeState` while the current snapshot advances to the latest transition?

## Change

Add one focused test using the existing `EvidenceRecord` and `LandscapeState` contracts. No Runtime or schema changes are introduced.

## Sequence

```text
Evidence A
   ↓
LandscapeState
   ↓
Evidence B
   ↓
Current Snapshot
```

## Expected observation

- Evidence A and Evidence B remain distinct records.
- Evidence A provenance/data is not overwritten by Evidence B.
- Existing list order makes the observed sequence addressable.
- The current snapshot reflects the latest applied transition.
- The current snapshot is not treated as a reconstruction of historical Evidence lineage.

## Non-goals

- Evidence query/indexing system
- Evidence lineage reconstruction
- event sourcing
- Provenance Graph
- historical state recovery
- new Runtime theory
- new Landscape schema

## Verification status

Implementation candidate only until the branch CI run is observed successful. File existence is not treated as experiment success.

## Integrity rule

No existing Evidence or observation record is rewritten. This experiment uses the existing `LandscapeState.evidence` list and `snapshot()` boundary unchanged.

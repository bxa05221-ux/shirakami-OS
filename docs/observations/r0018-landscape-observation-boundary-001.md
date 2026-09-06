# R0018 — Landscape Observation Boundary

## Purpose
Observe the boundary between the current Landscape snapshot and the preserved Evidence lineage.

## Observation question
Can the current Landscape snapshot be inspected as observable state without embedding or mutating the Evidence lineage?

## Scope
- Reuse existing `LandscapeState`.
- Apply existing Evidence records.
- Inspect `LandscapeState.snapshot()`.
- Verify preserved Evidence lineage remains unchanged.

## Non-goals
- semantic interpretation of Landscape state
- continuity or discontinuity detection
- historical identity
- replay semantics
- new Kernel/Evidence schema
- domain interpretation

## Expected boundary
`LandscapeState → snapshot` exposes the current observable state.

`LandscapeState.evidence` remains a separate preserved lineage.

The snapshot does not establish semantic continuity, semantic equivalence, or historical identity.

## Observation
The current implementation returns the state mapping from `snapshot()` while preserving the Evidence list separately. Reading the snapshot does not mutate the stored Evidence lineage.

## Conclusion
The observation boundary between current Landscape state and preserved Evidence lineage is inspectable with the existing Runtime model. No Runtime, ProtocolIR, or Evidence schema change is justified by this experiment.

# R0017 — Projection Re-observation Boundary

## Purpose
Observe whether the explicit Evidence → Landscape Projection boundary can be exercised repeatedly with the same Evidence sequence and produce the same observable Landscape snapshot.

## Observation question
Can the same ordered Evidence sequence, applied through `project_evidence()`, be re-observed as the same Landscape snapshot without Runtime inferring semantic continuity?

## Scope
- Reuse the existing `project_evidence()` boundary.
- Reuse existing `EvidenceRecord` instances.
- Apply the same ordered Evidence sequence to two independent `LandscapeState` instances.
- Compare resulting snapshots and preserved Evidence lineage.

## Expected boundary
`Evidence → project_evidence() → LandscapeState → snapshot()` is observable and reproducible.

The experiment does not establish historical identity, semantic equivalence, or continuity.

## Non-goals
- replay engine
- replay semantics
- semantic equivalence
- continuity scoring
- semantic continuity detection
- migration
- new Kernel/Evidence schema
- domain interpretation

## Observation
The explicit Projection boundary can be exercised independently on two Landscape states using the same ordered Evidence sequence. The resulting snapshots and observable Evidence ordering can be compared without adding continuity metadata.

## Conclusion
Current Projection behavior supports deterministic re-observation of the same Evidence sequence at the Landscape snapshot level. This remains an observation of current application behavior, not a claim about historical identity or semantic continuity.

No Runtime, ProtocolIR, or Evidence schema change is introduced.

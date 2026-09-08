# R0015 — Landscape Re-observation Boundary

## Purpose

Observe whether the existing Evidence → Landscape path can produce the same Landscape snapshot when the same ordered Evidence sequence is applied to equivalent empty Landscape states.

## Observation question

Can the same ordered Evidence sequence be re-observed as the same Landscape snapshot without Runtime inferring semantic continuity?

## Scope

- reuse the existing `LandscapeState.empty()` and `apply_evidence()` path
- reuse existing `EvidenceRecord` instances
- apply the same ordered Evidence sequence to two independent Landscape states
- compare the resulting snapshots and preserved Evidence lineage

## Expected boundary

`ordered Evidence → LandscapeState → snapshot` is observable and reproducible under the current implementation.

`re-observed snapshot → semantic continuity` is not established.

Re-observation here means only that the current state transition application yields the same observable state from the same Evidence sequence. It does not establish historical identity, semantic equivalence, migration correctness, or continuity across protocol versions.

## Non-goals

- replay engine
- replay semantics
- semantic equivalence
- continuity scoring
- semantic continuity detection
- migration
- new Kernel schema
- new Evidence schema
- domain interpretation

## Observation

The experiment applies three existing-style transition results to an Evidence sequence, then applies that same sequence to two independent empty Landscape states. The resulting snapshots are equal, while the ordered transition lineage remains observable in both states.

The experiment also verifies that neither `continuity` nor `continuity_claim` is introduced into the Landscape snapshot.

## Conclusion

The current Runtime path is sufficient to observe deterministic re-application of the same Evidence sequence at the Landscape snapshot boundary. No Runtime, ProtocolIR, or Evidence schema change is justified by this observation alone.

The remaining question is outside this experiment: what additional evidence, if any, would be required before a system could make a continuity claim. That question remains open and is not implemented by Shirakami OS Kernel.

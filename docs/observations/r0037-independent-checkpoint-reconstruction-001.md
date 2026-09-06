# R0037 Independent Checkpoint Reconstruction

## Purpose

Verify full replay and checkpoint-plus-delta re-observation equivalence when the checkpoint and applied Evidence are supplied as independently reconstructed inputs.

## Boundary

Independent checkpoint reconstruction → delta selection → re-observation

## Observation

The experiment reconstructs the observable checkpoint as a new mapping and the applied Evidence as a new ordered container before selecting delta Evidence. The resulting Landscape is compared with full ordered Evidence replay through the same Adapter observation boundary.

Equivalence is limited to the observable representation produced by the Adapter.

## Non-goals

- continuity claims
- identity claims
- inheritance claims
- provenance claims
- semantic interpretation
- truth determination
- Memory Manager changes
- backend semantics
- credential changes
- GitHub write semantics

## Next observation

Observe whether the same boundary remains stable when reconstructed inputs are produced from serialized representations, while keeping reconstruction distinct from continuity or identity evidence.

# R0036 Full Replay and Delta Re-observation Boundary

## Purpose

Verify that full ordered Evidence replay and checkpoint-plus-delta execution produce the same observable Landscape snapshot while making Evidence-lineage differences explicit.

## Boundary

Full Replay → Re-observation
Checkpoint + Delta → Re-observation

## Observation

The experiment compares the existing full Evidence replay path with the checkpoint-plus-delta path through the same module-level Landscape observation boundary.

Both paths reconstruct the same observable snapshot when the checkpoint represents the state after the already-applied Evidence and the remaining delta is applied.

The observation is **not** full representation equivalence: the full replay contains the complete local Evidence lineage, while the checkpoint-plus-delta path contains only the newly applied delta in its local Evidence list.

Therefore:

- snapshot equivalence is observed
- Evidence-lineage equivalence is not observed
- checkpoint state must not be treated as reconstructed history

## Non-goals

- semantic interpretation
- provenance claims
- continuity, identity, or inheritance claims
- truth determination
- Memory Manager changes
- backend semantics
- credential changes
- GitHub write semantics

## Next observation

Verify the same snapshot/lineage distinction when the checkpoint and applied Evidence are supplied as independently reconstructed inputs, without treating reconstruction as continuity or identity evidence.

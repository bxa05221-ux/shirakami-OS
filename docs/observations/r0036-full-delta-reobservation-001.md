# R0036 Full Replay and Delta Re-observation Equivalence

## Purpose

Verify that full ordered Evidence replay and checkpoint-plus-delta execution produce the same observable re-observation across multiple ordered transitions.

## Boundary

Full Replay → Re-observation
Checkpoint + Delta → Re-observation

## Observation

The experiment compares the existing full Evidence replay path with the checkpoint-plus-delta path through the same Adapter observation boundary. The Evidence input sequences are preserved. Equivalence is limited to the observable representation produced by the adapter.

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

Verify the same equivalence when the checkpoint and applied Evidence are supplied as independently reconstructed inputs, without treating reconstruction as continuity or identity evidence.

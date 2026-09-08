# R0034: Checkpoint + Delta Evidence execution boundary

## Purpose

Verify the smallest Runtime boundary that executes selected delta Evidence from an observable Landscape checkpoint.

## Observation

The execution entrypoint selects Evidence not already present in the supplied applied sequence, then replays only that delta against the supplied checkpoint snapshot.

The boundary preserves the existing replay model and does not infer semantic meaning from Evidence.

## Non-goals

- semantic interpretation
- provenance claims
- continuity claims
- identity or inheritance claims
- truth determination
- Memory Manager changes
- backend semantics
- credential handling
- GitHub writes

## Next observation

Verify that the checkpoint + delta execution entrypoint remains equivalent to full replay for multiple ordered transitions and does not mutate either Evidence input sequence.

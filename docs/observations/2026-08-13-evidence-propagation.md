# Observation: Evidence Propagation Experiment

## Status

Experimental verification on the β0.1 runtime boundary.

## Question

Can one immutable Evidence record propagate into multiple Landscape projections without the Evidence itself being mutated?

## Observed Structure

```text
Protocol
  ↓
Runtime
  ↓
Transition
  ↓
Evidence
  ├──→ Landscape A
  └──→ Landscape B
```

The experiment uses the existing `EvidenceRecord` and `LandscapeState` boundaries. No Foundation contract is changed.

## Observations

1. A completed Runtime execution can be captured as one `EvidenceRecord`.
2. The same Evidence can be applied independently to multiple `LandscapeState` instances.
3. The resulting Landscape snapshots can agree without sharing mutable state.
4. `EvidenceRecord` remains unchanged after Landscape projection.
5. Evidence whose transition is not marked as changed does not update Landscape state.

## Interpretation

This experiment supports a distinction between **Evidence as an immutable observed transition** and **Landscape State as a mutable projection of that transition**.

The experiment does not establish a new Foundation-level model. In particular, it does not yet define Evidence persistence, synchronization, conflict resolution, or a general observation protocol.

## Next Question

If the same Evidence is observed through different observation points, can the resulting projections intentionally differ while preserving a common Evidence identity?

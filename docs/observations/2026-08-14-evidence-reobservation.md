# Evidence Re-observation Experiment

## Status

Exploration / verification pending.

## Question

Can a projection produced from Evidence become a new observation without rewriting the original Evidence?

## Experimental lifecycle

```text
Runtime
  ↓
Evidence₁
  ↓
Propagation
  ↓
Landscape Projection
  ↓
Observation
  ↓
Evidence₂
```

## Expected properties

1. `Evidence₁` remains immutable.
2. The projection is local to the receiving Landscape.
3. Observation of that projection produces a distinct `Evidence₂`.
4. `Evidence₂` can retain a causal/reference relation to the preceding projection without mutating `Evidence₁`.
5. Failure or absence of a new transition remains observable without being promoted to transition evidence.

## Interpretation constraint

This experiment does not introduce a WaterVein abstraction.

The purpose is to determine whether an Evidence-to-Evidence lifecycle emerges naturally from the existing Runtime, Evidence, Landscape, Adapter, and Observation boundaries.

## Decision gate

If the lifecycle can be represented without changing the Foundation boundaries, the result supports treating propagation history as an observable relation.

If it cannot, the missing boundary is recorded as an architectural observation rather than immediately promoted to a new theory.

# Propagation Lifecycle Observation

## Status

Exploration / provisional observation.

## Question

Can a propagation path itself become observable evidence without introducing a dedicated `WaterVein` abstraction?

## Observation model

```text
Evidence
  ↓
Propagation
  ↓
Consumer
  ↓
Projection
  ↓
Observation
  ↓
new Evidence
```

The experiment treats the propagation path as a relation, not as a new data object.

## Working hypothesis

A persistent relation between an Evidence identity, its consumers, and resulting Landscape projections may exhibit water-vein-like behavior:

- the Evidence identity remains stable;
- propagation may branch;
- consumers may react differently;
- projections may become locally stable;
- later observations may produce new Evidence about the resulting projection;
- the original Evidence need not be rewritten.

## Important boundary

Do not introduce `WaterVein`, `Flow`, or equivalent domain classes at this stage.

The purpose is to determine whether the relation emerges naturally from existing Evidence, Propagation, Consumer, Projection, and Observation boundaries.

## Verification target

A successful observation would show a closed lifecycle in which a propagation result becomes observable again:

`Evidence → Propagation → Projection → Observation → Evidence`

If this cannot be represented with the current boundaries, that limitation is itself an observation to preserve.

## Interpretation

The water-vein concept remains a hypothesis. It is not promoted to Foundation terminology by this document.

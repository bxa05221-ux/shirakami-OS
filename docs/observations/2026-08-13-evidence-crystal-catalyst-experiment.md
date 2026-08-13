# Evidence Crystal / Catalyst Experiment

## Purpose

Test whether the same immutable Evidence record can exhibit two distinct behaviors in a Landscape:

1. **Crystal behavior** — Evidence provides a stable relational structure that later observations can attach to.
2. **Catalyst behavior** — Evidence causes or enables a transition in another Landscape or consumer without being consumed or modified itself.

## Provisional model

Evidence is not defined here as a fixed state such as ice, nor as a scalar temperature-dependent quantity.

Instead, Evidence is treated as an observation-derived structure whose behavior may include both:

- preservation of relations;
- propagation of change.

## Experiment A: Crystal behavior

Use one Evidence record `X` as a reference point for multiple Landscape projections.

Expected properties:

- `X` remains immutable.
- Multiple projections may preserve different relations to `X`.
- Later observations can establish additional relations without rewriting `X`.

## Experiment B: Catalyst behavior

Propagate the same Evidence record `X` to multiple consumers.

Expected properties:

- `X` is not consumed by propagation.
- Consumers may transition independently.
- Different consumers may produce different Landscape projections from the same `X`.
- A later observation creates a new Evidence record rather than modifying `X`.

## Combined hypothesis

If both experiments succeed, Evidence may be better understood as an **action point in Landscape** rather than as a fixed state.

Provisional formulation:

> Evidence is an observation-derived structure that can preserve relations and induce transitions while remaining immutable as a record.

This formulation is intentionally provisional and is not yet a Foundation-level contract.

## Non-goals

- No changes to `EvidenceRecord` fields.
- No persistence design.
- No formal three-state model.
- No temperature causality model.
- No Foundation revision.

## Verification target

The experiment should determine whether the existing β0.1 Evidence and Landscape boundaries are sufficient to represent both behaviors without introducing new semantic machinery.

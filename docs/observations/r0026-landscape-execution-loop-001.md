# R0026 — Landscape Execution Loop

## Purpose
Verify the minimal runtime loop after an external Landscape snapshot has been imported.

## Boundary

`LandscapeState (bootstrap) → Runtime → Transition → Evidence → LandscapeState`

## Observation

An already observed external snapshot can be used as the current Landscape state. A Protocol can then execute against bounded input, produce an observable `Transition`, be captured as immutable `Evidence`, and be applied to the same LandscapeState through the existing transition boundary.

The external bootstrap remains distinct from the Runtime transition. No external evidence lineage is imported as local Evidence.

## Acceptance

A test must demonstrate:

1. bootstrap an existing Landscape snapshot;
2. execute one Protocol through `Runtime`;
3. capture the resulting `ExecutionResult` as Evidence;
4. apply that Evidence to the existing LandscapeState;
5. observe the resulting state and Evidence lineage.

## Non-goals

- no GitHub write
- no credential changes
- no semantic interpretation
- no new Evidence schema
- no continuity or identity claim
- no AI-provider dependency

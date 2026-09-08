# R0048 — Interpretation Boundary Observation

## Question

Where does interpretation exist in the current Runtime boundary, and does the current Evidence/Projection implementation create a separate Interpretation record or lineage?

## Change

Add one deterministic boundary test using the existing Runtime, Evidence, LandscapeState, and Projection contracts. The test carries an explicitly named external interpretation value through an ordinary transition without changing the Evidence schema or Runtime semantics.

## Verification boundary

Observation + external interpretation value → Evidence → Projection

## Verification

- The current `EvidenceRecord` preserves the transition data that was explicitly supplied.
- The current Evidence contract does not expose a separate `interpretation` field.
- Projection carries the supplied transition data into the current Landscape state view.
- Projection does not create a separate Interpretation record.
- The observation does not infer whether the supplied interpretation is true, false, or semantically correct.

## Non-goals

- defining an Interpretation schema
- creating Interpretation Lineage
- semantic validation of interpretations
- converting interpretation into fact
- changing Evidence semantics
- Runtime theory changes
- human judgment

## Result boundary

A passing test demonstrates only the current implementation boundary: an interpretation-like value may exist as explicit transition data, while the current Evidence and Projection contracts do not separately own an Interpretation record or lineage.

This is an implementation observation, not a proposal to add an Interpretation subsystem.

## Architectural boundary

```text
Observed data
     ↓
Transition data
     ↓
EvidenceRecord
     ↓
Projection
     ↓
Landscape state
```

The current implementation does not establish a separate:

```text
InterpretationRecord
      ↓
InterpretationLineage
```

R0048 therefore records the boundary without inventing a new semantic layer.

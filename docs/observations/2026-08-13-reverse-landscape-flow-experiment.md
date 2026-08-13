# Reverse Landscape Flow Experiment α0.1

Date: 2026-08-13
Status: Implementation Experiment / Verification Pending

## Purpose

Test the smallest reverse path from a Landscape-derived Delta toward re-observation without allowing interpretation to overwrite Evidence.

This is an implementation experiment. It does not establish a Foundation contract or promote the Dark Question Layer to Runtime behavior.

## Experiment Flow

```text
Evidence
  ↓
Delta
  ↓
Matome Representation
  ↓
Dark Question
  ↓
Counter-Evidence
  ↓
Re-observation
```

## Boundaries

### Evidence

The existing `EvidenceRecord` remains immutable and is not modified by this experiment.

### Delta

`DeltaRecord` contains only observable mapping differences between two supplied snapshots. It does not infer meaning, cause, intent, or hidden state.

### Matome Representation

`MatomeRepresentation` wraps a Delta and records its representation format. YAML is the default experimental format, but the boundary does not require YAML.

### Dark Question

`DarkQuestion` records a question against the representation. The experiment deliberately does not generate a hidden answer.

### Counter-Evidence

`CounterEvidence` records a new observation supplied against the question. It is separate from the original Evidence.

### Re-observation

`ReObservation` creates a new lineage node. It links the new observation to prior Evidence without rewriting that Evidence.

## Verification Target

The experiment is successful if:

1. original Evidence remains unchanged;
2. Delta contains only observable differences;
3. Matome can represent Delta without becoming Evidence;
4. a Dark Question can exist without becoming an interpretation;
5. Counter-Evidence becomes a new observation rather than an amendment to the original Evidence;
6. Re-observation preserves lineage.

## Interpretation Constraint

This experiment does not decide whether a Dark Question is useful, correct, or sufficient for cognition. It only establishes a boundary in which questions can operate without silently converting interpretation into Evidence.

## Non-goals

- no change to `EvidenceRecord`;
- no LLM integration;
- no automatic interpretation generation;
- no Counter-Evidence ranking;
- no persistence model;
- no Foundation revision;
- no three-state model;
- no assumption that YAML is the canonical Matome language.

## Next Question

If the boundary remains stable, the next observation should compare a human-provided interpretation with an AI-generated interpretation and determine whether the same Evidence/Delta lineage can preserve both without collapsing them into one canonical claim.

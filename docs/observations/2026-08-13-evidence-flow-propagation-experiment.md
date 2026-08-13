# Evidence Flow Propagation Experiment α0.1

Date: 2026-08-13
Status: Implementation Experiment / Verification Pending

## Purpose

Test the next question from Landscape Flow Verification α0.1:

> Can one immutable Evidence event be propagated through multiple Landscape consumers while preserving a single transition meaning and a single observation point?

This experiment does not introduce a Foundation definition. It adds a minimal and reversible implementation boundary for observation.

## Experiment

The branch introduces `runtime/evidence_propagation.py` with:

- `EvidenceConsumer` as a minimal consumer contract
- `EvidencePropagator` as an explicit fan-out boundary
- propagation of the same `EvidenceRecord` object to each consumer

No existing Runtime, Evidence, Landscape State, or Adapter implementation is modified.

## Expected Observation

For one Runtime transition:

```text
Runtime
  ↓
EvidenceRecord
  ↓
EvidencePropagator
  ├──→ Landscape consumer A
  ├──→ Landscape consumer B
  └──→ ...
```

The experiment is successful if:

1. the same Evidence object reaches multiple consumers;
2. consumers can independently project the transition into their own state;
3. transition semantics are not duplicated or rewritten by the propagation layer;
4. failure evidence remains non-transition evidence;
5. existing β0.1 tests remain valid.

## Current Verification Status

The test suite has been added in `runtime/test_evidence_propagation.py`.

Execution through the repository CI is pending. No success claim is made until CI or an equivalent test execution provides evidence.

## Interpretation Constraint

A successful experiment does not establish a generalized fluid-data architecture.

It only establishes that an explicit propagation boundary can coexist with the current β0.1 state-transfer model without requiring a Foundation change.

A failed experiment is equally valuable: it would indicate that the current direct state-transfer boundary remains the more appropriate implementation shape.

## Next Observation

After verification, compare:

- direct `LandscapeState.apply_evidence()`
- direct `LandscapeAdapter.apply_transition()`
- multi-consumer `EvidencePropagator.propagate()`

The comparison should determine whether propagation deserves to remain an implementation helper, become a Design-level boundary, or be discarded.

# R0041 — Adapter Exchange Observation

## Question

Can the same Landscape be continued when the Adapter implementation is exchanged, without rewriting Evidence or changing the observed Landscape state?

## Scope

This experiment verifies only the Adapter exchange boundary.

### Change

- Add an observation test for Adapter A → Adapter B exchange.

### Verification

- Landscape state before exchange
- Landscape state after exchange
- Evidence remains available and unchanged
- Protocol provenance remains attached to the Evidence

### Not tested

- AI model quality or equivalence
- semantic reconciliation
- Evidence lineage reconstruction
- new Protocol semantics
- Landscape schema changes

## Existing boundary

The current LandscapeAdapter contract exposes `read_state()` and `apply_transition(evidence)`. The existing in-memory adapter is already used for boundary tests.

## Procedure

1. Execute the existing example Protocol through Runtime.
2. Capture the resulting Evidence.
3. Apply the verified transition through Adapter A.
4. Read the resulting Landscape state.
5. Instantiate Adapter B from that observed state.
6. Compare the state before and after the Adapter exchange.
7. Confirm that the original Evidence remains available with its Protocol identity and transition data.

## Expected observation

If the state remains identical and the Evidence object remains unchanged, the Adapter exchange boundary is operationally observable for this minimal case.

This document does not claim that all possible Adapters are interchangeable. It records only the result of this specific experiment.

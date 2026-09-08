# R0042 — Multi-Account Landscape Boundary Observation

## Question

Can Landscape state from multiple Accounts be connected to a Shared Landscape without merging the Account states or losing their provenance boundary?

## One Change / One Verification

R0042 adds a minimal observation test using the existing LandscapeAdapter boundary. Two independent Account states are observed through separate adapters and placed into a Shared Landscape structure keyed by Account identity.

## Scope

- Multiple Account Landscape states
- Account boundary preservation
- Evidence object separation
- Shared Landscape connection without state merge

## Explicitly not tested

- Authentication
- Cross-account authorization
- semantic reconciliation
- Evidence lineage reconstruction
- Account identity verification
- external AI equivalence
- persistent Shared Landscape storage

## Existing boundary

The current `LandscapeAdapter` exposes `read_state()` and `apply_transition(evidence)`. R0042 does not change that contract.

## Procedure

1. Execute the existing example Protocol independently for Account A and Account B.
2. Capture Evidence for each execution.
3. Apply each Evidence record through its own Landscape Adapter.
4. Read each resulting Landscape state independently.
5. Connect the two observed states into a Shared Landscape structure keyed by Account identity.
6. Confirm that each Account state remains distinct.
7. Confirm that the two Evidence objects remain distinct and retain Protocol provenance.

## Expected observation

If both Account states remain independently addressable and the Evidence objects remain separate, the minimal Shared Landscape connection boundary is observable without merging the Account states.

This document does not claim that arbitrary Accounts can be safely integrated. It records only the result of this specific experiment.

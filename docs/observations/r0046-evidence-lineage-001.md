# R0046 — Evidence Lineage Observation

## Question

Can equivalent Landscape state be observed without treating that state as a reconstruction of the original Evidence lineage?

## Change

Add one deterministic boundary test that executes two distinct Protocol identities against equivalent Landscape state and captures separate Evidence records.

## Verification boundary

Landscape state equality → Evidence provenance distinction

## Verification

- Landscape A and Landscape B expose equal state after the boundary exchange.
- Evidence A and Evidence B remain separately identifiable by Protocol provenance.
- Matching Landscape state is not used to infer that Evidence lineage has been reconstructed.
- Evidence records remain distinct immutable observations.

## Non-goals

- general Evidence lineage reconstruction
- semantic reconciliation
- historical Evidence recovery from Landscape state
- universal Protocol interoperability
- human judgment
- Runtime theory changes

## Result boundary

A passing test demonstrates only this minimal boundary: equivalent Landscape state can coexist with separately identifiable Evidence provenance. It does not establish that complete historical Evidence lineage can be reconstructed from Landscape state.

## Architectural boundary

Landscape State Reconstruction ≠ Evidence Lineage Reconstruction.

R0046 therefore observes the distinction rather than attempting to resolve it.

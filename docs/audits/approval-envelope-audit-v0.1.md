# Approval Envelope Audit v0.1

## Purpose

Assess whether Human Gate decisions can be carried across protocol transitions without being inferred, weakened, or silently expanded.

## Scope

Documentation and implementation-boundary audit. No Runtime semantics are changed.

## Required envelope fields

A future shared handoff envelope should explicitly preserve:

- `candidate_id` or route identity
- selected Protocol identifiers and versions
- reviewer identity or accountable role
- approval state
- approval scope and expiration, when applicable
- provenance and source Evidence references
- unresolved uncertainty and review notes
- revision or transformation history
- privacy, consent, and rights constraints
- execution authorization distinct from publication authorization

## Current observations

### Human Gate

The existing one-stroke route pipeline enters `HUMAN_REVIEW`, requires explicit approval, and refuses execution when the route is not authorized. Candidate generation remains separate from selection and authorization.

### Approval state

Approval is represented by Runtime state transitions, but a common serializable approval envelope shared by all protocol boundaries is not yet established.

### Scope preservation

The current route selection carries route identity, candidate Protocols, and reviewer information. Cross-protocol propagation of approval scope, expiration, rights constraints, and publication authority remains unverified.

### Evidence continuity

Human decisions and execution outcomes can be retained as Evidence in the existing route pipeline. End-to-end preservation of Evidence references through every transformation and renderer is not yet demonstrated.

### Fail-closed behavior

Existing tests cover rejection without approval, missing Protocol implementations, and mismatch handling. These tests do not by themselves establish that every future adapter or renderer will preserve the same boundary.

## Findings

- Human Gate behavior exists in a concrete route pipeline.
- Candidate generation is not equivalent to authorization.
- Runtime state is not yet a universal cross-protocol approval contract.
- Publication and execution authority must remain separate.
- Approval must not be inferred from successful rendering, adapter completion, or structural compatibility.

## Decision

Do not introduce automatic approval or a universal approval score. Treat the shared approval envelope as a separately specified contract before broad Runtime adoption.

## Follow-up priorities

1. Define a versioned, serializable approval envelope.
2. Specify allowed state transitions and fail-closed behavior.
3. Add transition fixtures for approval scope, provenance, uncertainty, and rights metadata.
4. Test that renderers and adapters cannot upgrade approval authority.
5. Record human decisions as Evidence with explicit provenance.

## Non-goals

- No automatic Protocol selection.
- No automatic execution or publication authorization.
- No replacement of domain-specific human review.
- No claim that current route tests prove universal cross-protocol enforcement.

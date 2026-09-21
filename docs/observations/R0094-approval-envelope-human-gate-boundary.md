# R0094 — Approval Envelope / Human Gate Boundary

## Scope

This observation records the focused boundary test introduced in PR #325.

## Verified intent

- Candidate identity and Protocol identity remain explicit.
- Provenance and Evidence references cross the envelope without granting authorization.
- Human approval creates a new authorized envelope rather than mutating the original.
- Execution authorization does not imply publication authorization.
- Unapproved candidates remain unauthorized.

## Non-goals

This observation does not claim full runtime integration. It does not select a Protocol, invoke a backend, or replace the existing Human Gate implementation.

## Next boundary

Integrate the envelope with the concrete route-selection and execution path only after the current Human Gate and ProtocolRequest contracts are mapped precisely.

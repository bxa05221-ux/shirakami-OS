# R0047 — Protocol Lineage Observation

## Question

Can Protocol identity remain the same while the exact Protocol artifact identity differs, without treating the artifacts as reconciled or equivalent?

## Change

Add one deterministic boundary test using the existing Protocol artifact SHA-256 hashing and mismatch detection boundaries.

## Verification boundary

Protocol identity → Protocol artifact identity → mismatch observation

## Verification

- A stable Protocol identity can be associated with distinct exact artifact bytes.
- Distinct artifact bytes produce distinct SHA-256 artifact identities.
- Each artifact can independently verify against its own hash.
- A historical hash compared with different current artifact bytes remains observable as a mismatch.
- No artifact reconciliation or semantic equivalence is inferred.

## Non-goals

- general Protocol lineage reconstruction
- semantic equivalence of Protocol artifacts
- historical artifact recovery
- universal Protocol version compatibility
- human judgment
- Runtime theory changes

## Result boundary

A passing test demonstrates only this minimal boundary: Protocol identity and exact Protocol artifact identity can remain separately observable, including an explicit artifact mismatch. It does not establish complete Protocol lineage reconstruction or semantic equivalence.

## Architectural boundary

Protocol Identity ≠ Protocol Artifact Identity ≠ Execution Evidence.

R0047 therefore observes the identity boundary without reconciling distinct artifacts.

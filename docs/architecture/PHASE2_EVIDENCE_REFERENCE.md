# Phase 2 — Evidence Reference Boundary

## Purpose

This boundary connects SemanticHandoff to the existing immutable Evidence identity model without collapsing Observation into Evidence.

## Rule

`Observation != EvidenceRecord`.

An observation may produce context and provenance. It becomes referenceable as Evidence only when a concrete `EvidenceRecord` exists.

The stable `evidence_id` belongs to that EvidenceRecord. The API and SemanticHandoff may carry an existing `evidence_id`; they do not manufacture one from an observation.

## Identity chain

```text
Observation
  -> observation_id

Concrete EvidenceRecord
  -> evidence_id (stable content-derived identity)

SemanticHandoff
  -> observation_id
  -> optional evidence_ids[]

API response
  -> transport only
```

## Why this matters

The existing Evidence identity work derives `evidence_id` deterministically from the complete canonical Evidence payload. Equivalent Evidence therefore has the same identity, while changed Evidence receives a different identity. This is the identity source for downstream provenance.

The SemanticHandoff must not duplicate that hashing rule. It references the identity supplied by the Evidence boundary.

## Current state

The Phase 2 API integration may legitimately return an empty `evidence_ids` collection when no concrete EvidenceRecord has been created for the observation.

That is not a failure and must not be silently converted into an EvidenceRecord.

## Authority

Evidence identity is provenance, not authority.

An `evidence_id` does not imply:

- approval;
- Human Gate completion;
- execution authorization;
- Protocol promotion;
- scope expansion.

> Observation can cross the boundary. Evidence can be referenced. Authority remains separate.

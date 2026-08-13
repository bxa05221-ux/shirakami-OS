# External Observation — Next Review Scope

Date: 2026-08-13
Status: Review Scope

This document defines the next review scope derived from the external observations of Sakana AI and Gemini.

No new Foundation theory is introduced.

## Multi-Observer Convergence

Sakana AI and Gemini independently surfaced substantially overlapping questions around:

- API / Runtime boundary consistency
- Evidence persistence responsibility
- Canonical GitHub Adapter boundary
- Runtime replaceability / conformance evidence

Gemini additionally raised Foundation / application-domain separation as a review question.

This convergence increases the priority of the shared questions, but does not establish any proposed solution as Foundation truth.

## Priority 1 — API / Runtime Boundary

Question:

Does every API operation that changes or exposes Landscape state need to pass through the Runtime boundary, or is there an intentionally separate read/control path?

Review method:

- compare `api/runtime_api.py` with Runtime and Landscape Adapter contracts
- identify which operations bypass Runtime
- determine whether the bypass changes Evidence or Landscape State semantics
- compare the repository evidence with both external observations
- record the result as an observation before modifying implementation

Decision outputs:

- aligned
- temporary implementation divergence
- architectural inconsistency

## Priority 2 — Evidence Persistence Responsibility

Question:

Who owns persistence of immutable Evidence?

Review method:

- trace Evidence creation
- trace current Landscape State application
- inspect Adapter and Backend responsibilities
- identify the smallest boundary that can preserve Evidence without making Runtime backend-dependent
- compare the result with the convergent external observations

No persistence implementation should be added until the responsibility boundary is observed and accepted.

## Priority 3 — Canonical GitHub Adapter Boundary

Question:

Why do the Runtime GitHub Landscape Adapter and Plugin GitHub Adapter both exist, and which boundary is canonical for β0.1 and later?

Review method:

- compare responsibilities
- compare callers
- compare read/write semantics
- compare authentication ownership
- identify duplication versus intentional separation
- compare the result with the convergent external observations

No consolidation should occur merely because the structures look similar.

## Secondary Review

After Priority 1–3:

- Runtime replaceability / conformance evidence
- Plugin → Runtime integration timing
- Foundation specification versus application-instance boundary

These remain secondary and should not expand the current implementation scope unless the primary review reveals a dependency.

## Completion Condition

The review is complete when each Priority 1–3 question has:

1. an observed repository fact,
2. an evidence reference,
3. an architectural interpretation,
4. external-observer comparison,
5. a decision status.

Only after that should implementation changes be considered.

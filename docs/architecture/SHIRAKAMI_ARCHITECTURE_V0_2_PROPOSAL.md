# Shirakami Architecture v0.2 — Canonical Change Proposal

Status: proposal / review required
Version: 0.2-draft

## Purpose

This document proposes a minimal normative extension to the existing Shirakami Architecture.

It does not replace Landscape First, Evidence, Protocol, Runtime, or Adapter boundaries.

It makes the authority and state-transition boundary explicit.

## 1. Canonical state transition

The canonical state transition is:

Reality
→ Observation
→ Model Analysis
→ Proposal
→ Human Gate
→ Landscape
→ Projection
→ Renderer
→ User

A Model may analyze observations and generate proposals.

A Model does not directly write canonical accepted Landscape state.

## 2. Human Gate

Human Gate is the authority boundary for accepted Landscape state.

A proposal must be explicitly:

- accepted;
- rejected; or
- revised.

Only acceptance advances canonical accepted state.

## 3. Proposal

A Proposal is non-authoritative candidate state.

Model output, renderer output, or other generated material does not become canonical state merely because it was generated.

## 4. Projection

Projection is a read-side boundary between Landscape and Renderer.

It selects a perspective, observation axis, context, and presentation parameters.

Projection is not a second source of truth.

## 5. Renderer

Renderer expresses a Projection.

Renderer must not mutate canonical Landscape state.

A Landscape may therefore be rendered through multiple independent Renderers without changing the underlying accepted state.

## 6. Provenance

Accepted state must remain traceable to its transition sources, including where applicable:

Proposal
→ Observation / Evidence
→ source Model / Runtime
→ handoff
→ Human Gate decision

Rejected proposals do not become accepted state.

## 7. Implementation substitution

Model, Runtime, Adapter, Projection, and Renderer are replaceable implementation components.

Replacing one component must not transfer authority away from Landscape and Human Gate.

This property should be verified through conformance tests rather than assumed from implementation structure.

## 8. Mismatch

A mismatch between expected and observed state is Evidence for investigation.

A mismatch does not automatically authorize a Model or Runtime to alter normative architecture.

The evolution loop remains:

Implementation
→ Observation
→ Evidence
→ Verification
→ Mismatch
→ Research
→ Specification
→ Human Gate
→ Implementation

## 9. Compatibility

This proposal is additive to the existing public architecture.

It does not require:

- a new AI model;
- a specific vendor;
- ThreadRPG;
- a specific programming language;
- a specific storage implementation.

It preserves the existing principles:

- Landscape First;
- Evidence as a first-class boundary;
- Protocol / Specification;
- Runtime replaceability;
- Adapter separation;
- Human Gate;
- model independence.

## 10. Scope exclusions

The following are deliberately not normative architecture:

- ThreadRPG-specific classes;
- Python module layout;
- GitHub workflow names;
- response-count test values;
- experimental branch names;
- implementation-specific adapter classes;
- laboratory fixtures;
- private/core semantic material.

## 11. Verification basis

The proposal is based on the Landscape Runtime laboratory work.

Verified laboratory criteria:

- C-001 through C-012;
- RT-001 through RT-010;
- Landscape Runtime Position;
- Architecture Alignment;
- Canonical Promotion Gate;
- Canonical Promotion Delta Audit;
- Shirakami Architecture v0.2 draft.

The laboratory evidence is supporting evidence for this proposal, not a replacement for repository-level review.

## 12. Review boundary

This document is a proposed canonical change.

Creating this proposal does not modify canonical architecture on `main`.

Final adoption requires:

1. repository review;
2. CI verification;
3. explicit Human Gate approval;
4. merge through the repository's normal controls.

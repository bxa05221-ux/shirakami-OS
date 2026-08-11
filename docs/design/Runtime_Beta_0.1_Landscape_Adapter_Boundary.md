# Runtime β0.1 Landscape Adapter Boundary

Status: Design Draft
Version: 0.1
Date: 2026-08-11

## 1. Purpose

Define the smallest replaceable boundary between Runtime-managed Landscape operations and an external Landscape backend.

This document does not define GitHub-specific behavior and does not establish a new Foundation-level Landscape Contract.

## 2. Boundary

The Runtime interacts with Landscape through a narrow adapter capability:

Runtime
↓
Landscape Adapter
↓
External Landscape

The Runtime core must not know whether the external Landscape is a repository, file store, database, service, or another implementation.

## 3. Minimal Operations

The β0.1 prototype requires only:

- `read_state()` — obtain current observable Landscape state;
- `apply_transition()` — apply an explicitly verified Landscape transition.

Persistence, synchronization, conflict resolution, and authentication are outside this boundary.

## 4. Evidence Rule

The Adapter must receive a transition that has already passed the Runtime Evidence boundary.

The Adapter must not reinterpret arbitrary execution output as a Landscape change.

Conceptually:

Protocol
→ Transition
→ Evidence
→ Landscape Adapter
→ External Landscape

## 5. Replaceability Test

A conforming adapter can be replaced without changing Protocol execution semantics.

The prototype should therefore provide an in-memory external Landscape implementation and a second adapter implementation only when needed to demonstrate replacement.

## 6. Explicit Non-Goals

- GitHub API semantics
- repository commits
- synchronization protocol
- conflict resolution
- distributed transactions
- authentication
- authorization
- database persistence

## 7. Verification

The boundary is valid if the Runtime can:

1. execute a Protocol;
2. produce immutable Evidence;
3. send only a verified transition to the Landscape Adapter;
4. observe the resulting external Landscape state;
5. replace the adapter implementation without modifying Protocol semantics.

## 8. Architectural Invariant

Landscape remains the architectural asset.

The Adapter is a replaceable connection to Landscape storage or representation.

Runtime remains a service that executes Protocols and orchestrates observable transitions.

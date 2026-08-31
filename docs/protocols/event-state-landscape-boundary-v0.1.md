# Event → State → Landscape Boundary Test v0.1

## Purpose

Verify the implementation boundary between Event, State Projection, Evidence, and Landscape without assigning domain meaning to the Runtime.

## Contract

```text
Event
  ↓
State Projection
  ↓
Evidence
  ↓
Landscape
```

The Runtime may execute a transition and preserve observable data. It must not invent domain interpretation.

## Required invariants

- Event data remains observable after projection.
- Evidence preserves the original transition data.
- Landscape can apply Evidence without interpreting symbolic/domain identity.
- Protocol metadata remains separate from domain meaning.
- The Runtime does not become the owner of Landscape semantics.

## Non-goals

This document does not introduce a new domain model, event-sourcing framework, or semantic interpretation layer. It records an implementation boundary to be tested by the existing Runtime and Evidence contracts.

## Expected test direction

A minimal bridge test should construct an observable transition, capture Evidence, apply it to an empty LandscapeState, and verify that the relevant observable fields survive unchanged.

```text
transition
  → execution.result
  → capture_evidence(...)
  → LandscapeState.apply_evidence(...)
  → preserved observable state
```

If information is lost, the test should identify the exact boundary at which it disappears rather than compensating by adding interpretation to the Runtime.

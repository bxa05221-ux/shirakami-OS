# Protocol Route Foundation

## Purpose

This implementation begins the post-MVP Protocol operational layer without
changing the normative Protocol contract.

Matome YAML remains the canonical human-authored representation of a Protocol.
The Runtime specification already defines Protocol as an executable description
and identifies Matome YAML as its canonical authoring form.

## Design

A Protocol is treated as a registered artifact that can be selected through a
small parameterized invocation request. The API boundary is generic; it does
not create one endpoint per Protocol.

```text
Matome YAML
    ↓
Protocol Registry
    ↓
Protocol Request
    ↓
Generic invocation surface
    ↓
Injected executor / Runtime adapter
```

The Route Map is a separate observable routing structure. It has two related
operations:

```text
Declared route:
Protocol A ──→ Protocol B

Observed route:
Protocol A ──→ Protocol B
      └──────────── recorded after traversal
```

A declared edge may be traversed explicitly with `move()`. An observed move
may be recorded with `record_transition()`. Recording does not infer a route,
choose a semantic destination, or change Protocol meaning; it preserves the
fact that a traversal occurred and makes the resulting location current.

## Current implementation

- `runtime/protocol_registry.py` stores Protocol artifacts and lifecycle state.
- `runtime/protocol_api.py` resolves a registered Protocol into a parameterized request and dispatches it through an injected executor.
- `runtime/route_map.py` stores current location, explicit Protocol edges, and observed traversals.

The generic API does not know how execution is performed. An executor can be
supplied by the Runtime or by an external application. This keeps the Protocol
surface independent of any particular LLM, backend, or UI.

## Route principle

The Route Map is not a prediction of the future. It is an observable record of
where the system is and which Protocol relationships have been declared or
observed.

In operational terms:

```text
前に道はない
    ↓
Protocol execution
    ↓
Observable transition
    ↓
Route observation
    ↓
後ろに道ができる
```

## Non-goals

- replacing Matome YAML with a new authoring format
- embedding Protocol meaning in the Runtime Kernel
- creating Protocol-specific HTTP endpoints
- defining a universal cognitive ontology
- defining semantic route selection
- changing Evidence or Landscape schemas
- selecting an AI provider

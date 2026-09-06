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
Runtime
```

The Route Map is a separate observable routing structure:

```text
Protocol A ──→ Protocol B
     │             │
     └────────────→ Protocol C
```

It records the current Protocol location and explicitly reachable Protocols.
It does not interpret their domain meaning.

## Current implementation

- `runtime/protocol_registry.py` stores Protocol artifacts and lifecycle state.
- `runtime/protocol_api.py` exposes a generic parameterized Protocol request.
- `runtime/route_map.py` stores current location and explicit Protocol edges.

The Route Map deliberately starts with only three operations: inspect the
current location, list reachable Protocols, and move along an explicit edge.

## Non-goals

- replacing Matome YAML with a new authoring format
- embedding Protocol meaning in the Runtime Kernel
- creating Protocol-specific HTTP endpoints
- defining a universal cognitive ontology
- defining semantic route selection
- changing Evidence or Landscape schemas
- selecting an AI provider

## Next concrete use

The next practical step is to register real existing Matome Protocol artifacts
and expose a single generic invocation surface to a small external application,
such as a chatbot. The Route Map can then be populated from actual Protocol
relationships rather than from hypothetical architecture.

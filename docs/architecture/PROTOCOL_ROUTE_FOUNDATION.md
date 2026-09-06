# Protocol Route Foundation

## Purpose

This implementation begins the post-MVP Protocol operational layer without
changing the normative Protocol contract.

Matome YAML remains the canonical human-authored representation of a Protocol.
The Runtime specification already defines Protocol as an executable description
and identifies Matome YAML as its canonical authoring form.

## Protocol lifecycles

Shirakami OS has two Protocol lifecycles. They use the same Protocol machinery;
the difference is lifetime and ownership.

```text
Protocol
│
├── Default Protocol
│     └── permanent OS foundation
│
└── Temporary Protocol
      └── user-authored Matome YAML
            ├── register
            ├── invoke
            ├── replace
            └── remove
```

The Default Protocol is mandatory at the OS operational boundary. There is one
Default Protocol, it remains available as the permanent base behavior, and it
cannot be removed or replaced through the temporary lifecycle.

A Temporary Protocol is an ordinary Protocol artifact with a shorter lifecycle.
A user may first work through an interaction flow without explicitly designing
a Protocol. Once the flow has stabilized, the user may express that flow as
Matome YAML and register the resulting artifact as a Temporary Protocol. It can
then be invoked, replaced when the working flow changes, and removed when it is
no longer needed.

This is a lifecycle distinction, not a semantic hierarchy: both are resolved
into the same generic `ProtocolRequest` and are executed through the same
injected executor boundary.

## Stabilized flow to Temporary Protocol

The authoring boundary is deliberately explicit but lightweight:

```text
ordinary interaction
        ↓
working flow stabilizes
        ↓
Matome YAML is created
        ↓
parse / validate
        ↓
Temporary Protocol registration
        ↓
reuse / replace / remove
```

The Runtime does not infer when a flow has stabilized and does not generate the
Matome YAML. The user-authored Matome YAML is the artifact that crosses the
Protocol boundary. This preserves the distinction between observed interaction
history and an explicitly authored reusable Protocol.

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
      └──────────── recorded after dispatch
```

A declared edge may be traversed explicitly with `move()`. An observed move
may be recorded with `record_transition()`. Recording does not infer a route,
choose a semantic destination, or change Protocol meaning; it preserves the
fact that the generic Protocol invocation surface dispatched the requested
Protocol and makes that destination current.

This is deliberately a **dispatch-level route observation**. It is not yet a
second execution result or a replacement for Runtime Evidence. The executor
remains the authority for execution semantics and the existing Runtime remains
the authority for Observable Transition and Evidence.

## Current implementation

- `runtime/protocol_registry.py` stores Protocol artifacts and their lifecycle.
- `runtime/protocol_api.py` resolves either the mandatory Default Protocol or a registered Protocol into a parameterized request and dispatches it through an injected executor.
- `runtime/protocol_api.py` also converts validated Matome YAML into a registered Temporary Protocol artifact.
- `runtime/route_map.py` stores current location, explicit Protocol edges, and observed dispatches.

The generic API does not know how execution is performed. An executor can be
supplied by the Runtime or by an external application. This keeps the Protocol
surface independent of any particular LLM, backend, or UI.

## Boundary to Runtime observation

The existing Runtime already produces an `ExecutionResult` containing the
Protocol ID and an observable `Transition`. Evidence is captured from that
result without rewriting the transition data.

Therefore the architectural direction is:

```text
Default / Temporary Protocol
            ↓
      ProtocolRequest
            ↓
Runtime / injected executor
            ↓
      ExecutionResult
        ├──→ Evidence → Landscape
        └──→ route observation boundary
```

The Route Map must not duplicate Evidence or reinterpret transition data. A
future integration may project an already-observed execution into the Route
Map, but this foundation keeps that projection at the boundary rather than
coupling the generic Protocol API to Kernel internals.

## Route principle

The Route Map is not a prediction of the future. It is an observable record of
where the system is and which Protocol relationships have been declared or
dispatched.

In operational terms:

```text
前に道はない
    ↓
Protocol dispatch
    ↓
Runtime execution
    ↓
Observable transition / Evidence
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

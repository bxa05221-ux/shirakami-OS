# Adapter Contract α0.1

## Status

This document defines the minimum boundary between Shirakami OS Runtime and an external Backend or service.

It is intentionally minimal and records the current architectural boundary. It does not define a universal plugin system or require support for every possible Backend.

## 1. Purpose

An Adapter connects the Runtime to a Backend while preventing Backend-specific behavior from becoming part of Runtime Core.

The current architectural direction is:

```text
Landscape
   ↓
Protocol
   ↓
Runtime
   ↓
Adapter
   ↓
Backend
```

## 2. Adapter Responsibilities

An Adapter is responsible for translating between Runtime-level operations and Backend-specific operations.

At minimum, an Adapter may provide:

- read access to Backend state required by an active operation;
- controlled write operations explicitly permitted by the Runtime and active Protocol;
- translation of Backend events or results into Runtime-observable forms;
- preservation of Backend provenance needed for Evidence.

## 3. Runtime Responsibilities

Runtime Core must not require knowledge of GitHub-specific, database-specific, filesystem-specific, or other Backend-specific APIs in order to execute a Protocol.

Runtime remains responsible for:

- Protocol execution;
- transition control;
- Evidence recording;
- Landscape State exposure;
- enforcing Runtime-level write boundaries.

## 4. Controlled Write

Adapters must not be treated as unrestricted write channels.

A write should occur only when:

1. the Runtime has an operation that permits the write;
2. the active Protocol permits or requires the transition;
3. the Adapter can represent the operation in the target Backend;
4. sufficient Evidence/provenance can be preserved.

The Adapter must not independently invent transitions.

## 5. Read-back

When a controlled write changes Backend state, the Adapter should support read-back or equivalent observation so that the resulting state can be compared with the intended transition.

Conceptually:

```text
Runtime Intent
     ↓
Controlled Write
     ↓
Backend
     ↓
Read-back / Observation
     ↓
Evidence
```

## 6. Backend Independence

The contract does not require all Backends to expose identical capabilities.

Instead, an Adapter declares or exposes the capabilities that it can safely support.

A Runtime must not assume that a capability exists merely because another Adapter provides it.

## 7. GitHub Adapter

GitHub is the current Backend used by the Shirakami OS implementation.

The GitHub Adapter is therefore the first concrete implementation of this boundary. Its existence does not make GitHub a required architectural dependency of Runtime Core.

## 8. Evidence and Provenance

Backend-originated observations that affect Landscape State should retain enough provenance to identify the Backend context and relevant operation.

The Adapter translates Backend facts; it does not rewrite them into architectural conclusions.

## 9. Not Defined by α0.1

This contract does not yet define:

- a universal plugin lifecycle;
- authentication implementation;
- authorization policy language;
- conflict-resolution algorithms;
- synchronization protocols between arbitrary Backends;
- a mandatory capability schema;
- automatic multi-Backend orchestration.

Those concerns require further observation and specification.

## 10. Compatibility Rule

An Adapter claiming α0.1 compatibility must:

1. remain behind the Runtime/Adapter boundary;
2. expose only operations it can safely perform;
3. honor controlled-write constraints;
4. support observation/read-back where required by the operation;
5. preserve relevant Backend provenance for Evidence;
6. avoid embedding Backend-specific assumptions into Runtime Core.

## 11. Evolution

This contract should grow only when implementation or observation demonstrates a stable cross-Backend requirement.

The goal of α0.1 is not maximum abstraction. The goal is a stable, testable boundary around the current Runtime.

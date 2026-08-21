# Supabase Adapter α0.1

## Purpose

The Supabase Adapter provides an external persistence boundary for Shirakami Landscape, Evidence, Context, and observed Relations.

It is an experimental adapter. Supabase is a Backend, not part of Runtime Core.

## Architectural position

```text
Landscape
   ↓
Protocol
   ↓
Runtime
   ↓
Supabase Adapter
   ↓
Supabase / PostgreSQL
```

The Adapter translates Runtime-level operations into Backend operations and preserves Backend provenance for Evidence.

## α0.1 scope

The first experiment intentionally stores only four conceptual objects:

- `landscape` — an observable context container;
- `evidence` — an immutable observation record;
- `context` — human-readable contextual material associated with an object;
- `relation` — an observed or candidate connection between two objects.

A `relation` is **not an AI conclusion**. It records that a connection was observed or proposed, together with its provenance and status.

## Water-vein principle

The Adapter is designed to support a distinction between:

```text
surface statement
      ↓
observable context
      ↓
relations
      ↓
possible shared context
```

The system must not silently convert a relation into a claim about a person's true intention.

## Write boundary

The Adapter must not invent transitions. Writes must originate from an allowed Runtime operation and active Protocol, with enough provenance to support later observation/read-back.

## Japanese context

Text is stored as UTF-8. No translation or normalization of Japanese prose is performed by the Adapter. Original text is preserved as supplied by the Runtime.

## Status

Experimental / α0.1

This document does not yet define authentication, authorization policy, synchronization, conflict resolution, or a universal Backend capability model.

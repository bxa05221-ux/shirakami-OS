# Shirakami Phase 2 — Semantic Handoff Boundary

Status: **Phase 2 implementation boundary candidate**

## Purpose

The API boundary and the Runtime boundary must exchange a stable semantic handoff without making transport data authoritative.

The handoff is a carrier of already-known context. It is not an approval mechanism, a Protocol promotion mechanism, or a new execution authority.

## Handoff contents

A semantic handoff may carry:

- `observation_id` — identity of the observation at the external boundary;
- `landscape` — immutable snapshot of relevant Landscape context;
- `protocol_id` — explicit Protocol reference, when one exists;
- `runtime_state` — observed Runtime state at handoff time;
- `evidence_ids` — references to Evidence already known at handoff time;
- `metadata` — provenance/context metadata.

## Authority boundary

The handoff MUST NOT contain or infer:

- approval;
- Human Gate result;
- execution authorization;
- scope expansion;
- candidate promotion;
- provider authority.

If execution authorization is required, it must arrive through the existing Approval Envelope / Activation boundary.

## Immutability

The semantic handoff is frozen after creation.

Consumers may derive new context from it, but must not mutate the original handoff or reinterpret it as a new authorization artifact.

## Relationship to ContextSnapshot

`ContextSnapshot` remains the Runtime's existing immutable execution-context structure.

`SemanticHandoff` is the explicit cross-boundary envelope around that context. This keeps transport identity/provenance separate from Runtime execution context.

## Principle

> Context may cross the boundary. Authority may not.

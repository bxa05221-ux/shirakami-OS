# Shirakami Phase 2 — Semantic Handoff Boundary

Status: **Phase 2 implementation boundary — API observe + stable Evidence identity integrated**

## Purpose

The API boundary and the Runtime boundary must exchange a stable semantic handoff without making transport data authoritative.

The handoff is a carrier of already-known context. It is not an approval mechanism, a Protocol promotion mechanism, or a new execution authority.

## Handoff contents

A semantic handoff may carry:

- `observation_id` — identity of the observation at the external boundary;
- `landscape` — immutable snapshot of relevant Landscape context;
- `protocol_id` — explicit Protocol reference, when one exists;
- `runtime_state` — observed Runtime state at handoff time;
- `evidence_ids` — stable `EvidenceRecord.evidence_id` references created by the observation boundary;
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

## API integration

`ShirakamiAPI.observe()` creates a fresh `observation_id` and returns a `semantic_handoff` alongside the existing state/evidence response.

The handoff now carries the stable `EvidenceRecord.evidence_id` values produced by the observation call. The API evidence serialization exposes the same identity, so the reference can be traced from Evidence → SemanticHandoff → HTTP without introducing a new authority field.

The integration is intentionally one-way with respect to authority:

- observation identity is generated at the external semantic boundary;
- ContextSnapshot fields are copied into the handoff;
- stable Evidence identity is referenced, not regenerated, at the handoff boundary;
- no approval, Human Gate result, execution authorization, promotion, or scope expansion is added to the handoff.

# Shirakami Phase 2 — Semantic Handoff Boundary

Status: **Phase 2 implementation boundary — API observe + stable Evidence identity integrated**

## Purpose

`SemanticHandoff` is an immutable context envelope crossing the semantic boundary. It carries context and references to Evidence without becoming an authority artifact.

A semantic handoff may carry:

- `observation_id` — identity of the observation occurrence;
- `landscape` — immutable snapshot of relevant Landscape context;
- `protocol_id` — explicit Protocol reference, when one exists;
- `runtime_state` — observed Runtime state at handoff time;
- `evidence_ids` — stable `EvidenceRecord.evidence_id` references created by the observation boundary;
- `metadata` — provenance/context metadata.

## Authority boundary

The handoff must not contain approval, Human Gate result, execution authorization, promotion, scope expansion, or provider authority.

## API integration

`ShirakamiAPI.observe()` creates a fresh `observation_id` and returns a `semantic_handoff` alongside the existing state/evidence response.

The handoff carries stable `EvidenceRecord.evidence_id` values produced by the observation call. The API evidence serialization exposes the same identity, so the reference can be traced from Evidence → SemanticHandoff → HTTP without introducing a new authority field.

The integration is intentionally one-way with respect to authority:

- observation identity is generated at the external semantic boundary;
- ContextSnapshot fields are copied into the handoff;
- stable Evidence identity is referenced, not regenerated, at the handoff boundary;
- no approval, Human Gate result, execution authorization, promotion, or scope expansion is added to the handoff.

## Principle

> Context may cross the boundary. Authority may not.

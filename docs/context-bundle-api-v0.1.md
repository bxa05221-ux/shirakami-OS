# Context Bundle API v0.1

## Purpose

Evolution API v0.1 now admits request-scoped context when explicit
`evidence_ids` are supplied.

## Execution boundary

`HTTP Request -> Context Routing -> Evidence Resolver -> Context Bundle -> Evolution Runtime -> Backend -> Evidence`

The API accepts the caller's explicit context references and an in-memory
Evidence store for v0.1. Only successfully resolved records are admitted to
the Backend handoff.

## Invariants

- No `evidence_ids` means existing API behavior is preserved.
- Supplied Evidence IDs are resolved exactly in declared order.
- A missing requested Evidence record fails the request.
- Unrequested Evidence never enters the Context Bundle.
- The Evidence store is removed before the Backend receives the handoff.
- Request-scoped lineage is exposed separately from Evidence content.
- Context admission does not create authority or a Decision.

## Principle

The API boundary is now a Context Routing boundary:

> The model does not receive the conversation by default.
> It receives only the context explicitly admitted for this request.

# Evidence Resolver v0.1

## Purpose

Evidence Resolver turns the explicit Evidence IDs selected by Context Routing
into concrete Evidence records for one request.

## Boundary

`Request -> Context Routing -> Evidence Resolver -> SemanticHandoff -> Runtime -> Backend -> Evidence`

The resolver is intentionally deterministic and reference-based.

## Rules

- Resolve only explicitly requested Evidence IDs.
- Preserve the request's declared order.
- Do not perform semantic search or ranking.
- Do not add unrequested records.
- Do not silently drop a missing requested record.
- Preserve request-scoped lineage.
- Resolution does not grant authority to the resolved record.

## Failure behavior

If a requested Evidence ID is absent from the supplied store,
`EvidenceResolutionError` is raised. This makes missing context observable
instead of allowing a Runtime request to proceed with an incomplete context.

## v0.1 scope

This is an in-memory/reference-store primitive. Persistent storage,
authorization, semantic retrieval, ranking, caching, and provider-specific
memory APIs remain outside this boundary.

## Design principle

> Context Routing decides **which references** are needed.
> Evidence Resolver decides **whether those references actually exist**.
> Runtime decides **what to execute**.
> Human Gate remains responsible for human judgment.

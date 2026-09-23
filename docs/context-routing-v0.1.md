# Context Routing v0.1

## Purpose

Context Routing controls **which external context is supplied to a Runtime
request**. It is deliberately different from enlarging a model's context
window or replaying an entire conversation.

## Boundary

`Request -> Context Routing -> SemanticHandoff -> Runtime -> Backend -> Evidence`

The router is request-scoped and reference-based.

## Rules

- Do not replay the entire conversation by default.
- Do not search or infer hidden model memory.
- Select only explicitly referenced Evidence, Protocol, and Runtime records.
- Preserve the request ID across the selected context.
- Treat selected context as references, not as authority.
- Missing references remain missing; the router does not invent them.
- Human judgment remains outside the routing layer.

## Minimal contract

Input:

```yaml
request_id: req-001
evidence_ids:
  - e-001
protocol_ids:
  - p-001
runtime_ids:
  - r-001
```

Output:

```json
{
  "request_id": "req-001",
  "evidence_ids": ["e-001"],
  "protocol_ids": ["p-001"],
  "runtime_ids": ["r-001"]
}
```

## Design principle

> Context Window != Context.

The Runtime should answer the narrower question:

> **What context does this request need now?**

rather than:

> How much of the previous conversation can the model read?

## v0.1 scope

This version performs explicit reference routing only. It does not yet
implement a persistent store, semantic retrieval, ranking, authorization,
or provider-specific memory APIs. Those belong to later boundaries.

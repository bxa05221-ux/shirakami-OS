# Context Bundle v0.1

## Purpose

Context Bundle is the concrete, request-scoped boundary of context admitted to
the Runtime. It contains only references selected by Context Routing and
Evidence records successfully resolved by Evidence Resolver.

## Boundary

`Request -> Context Routing -> Evidence Resolver -> Context Bundle -> SemanticHandoff -> Runtime -> Backend -> Evidence`

## Invariants

- One request ID identifies the bundle.
- Evidence IDs must exactly match the routed Evidence selection and order.
- Every resolved Evidence record must carry the same request ID.
- Protocol and Runtime references come only from the Context Selection.
- No unrelated memory or unrequested records enter the bundle.
- Bundle construction does not grant authority.
- Human judgment remains outside the bundle.

## Design principle

> Context Window is capacity.
> Context Routing is selection.
> Evidence Resolver is existence.
> Context Bundle is admission.

The model receives the admitted context, not the entire historical context by
default.

# Prompt Assembly Protocol

## MVP status

Draft v0.1 — executable assembly slice.

## Purpose

Prompt Assembly converts an explicit State-to-Protocol routing result into a
versioned Runtime input.

It does not invoke an AI provider and it does not make a human decision.

## Flow

```
Evidence
  ↓
Context
  ↓
3D Matrix
  ↓
Protocol Routing
  ↓
Prompt Assembly
  ↓
Runtime
```

## Prompt boundary

A Prompt is an execution representation, not a memory store.

Each assembled Prompt records:

- Prompt ID and version
- selected Protocol
- Runtime target
- Matrix state
- Context version
- Evidence references
- Uncertainty
- execution constraints

## Safety boundary

The MVP Prompt Assembly layer explicitly carries:

- Evidence as references, not invented facts;
- Simulation/Reality separation;
- unknown or unresolved information;
- the human decision boundary.

A blocked routing result cannot be assembled into an executable Prompt.

## Reconstruction

The Prompt must be traceable back to the Routing event that produced it.
The later full implementation should therefore attach:

```
Routing Event ID
  ↓
Prompt ID / Version
  ↓
Runtime ID / Version
```

This permits reconstruction of which Prompt was assembled from which state.

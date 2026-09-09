# R0058 — Renderer Exchange Operational Verification

## Status

Experimental observation record for Shirakami OS β1.0 operation.

## Purpose

Observe whether a Landscape can be presented through different Renderer boundaries without changing the underlying Landscape, Evidence, or Protocol state.

## Scope

- Record the operational start of Renderer Exchange verification.
- Treat Renderer as a presentation boundary over existing Landscape state.
- Verify that changing Renderer does not imply rewriting Landscape or Evidence.
- Reuse the existing β1.0 Runtime verification path and protected `main` merge route.

## Boundary under observation

```text
Landscape
   ↓
Runtime
   ↓
Renderer A
   ↓
Renderer exchange
   ↓
Renderer B
```

The observation concerns boundary continuity, not output quality or semantic equivalence between rendered representations.

## Non-goals

- AI/model quality evaluation
- Renderer output quality ranking
- semantic equivalence of rendered text/images/audio
- new Protocol semantics
- Landscape schema changes
- Evidence lineage reconstruction
- Runtime semantic changes
- automatic interpretation of Renderer output

## Verification rule

One Change / One Verification.

A successful Renderer execution must not be inferred merely from the existence of a Renderer artifact. The canonical `test-runtime` check remains the required merge gate.

## Expected observation

If Renderer A and Renderer B consume the same observable Landscape boundary, the Renderer exchange should not by itself mutate the Landscape or rewrite historical Evidence.

Any discrepancy that cannot be established from observable repository/runtime state remains unresolved rather than being inferred away.

## Theoretical boundary

No new theory is introduced by this observation. If the operational test exposes a theoretical ambiguity concerning Renderer semantics, that issue is returned to the research side.

# R0019 — Landscape Adapter Boundary

## Observation target

Can the current `LandscapeState` and accumulated Evidence lineage be exposed through a backend-agnostic Adapter without Runtime inferring semantic meaning?

## Scope

- Reuse existing `LandscapeState.snapshot()`.
- Reuse existing accumulated `EvidenceRecord` instances.
- Expose the current snapshot and ordered Evidence lineage through `adapt_landscape_observation()`.
- Preserve protocol and transition identity.
- Verify that no continuity claim is produced.

## Observed boundary

The Adapter can expose the current observable Landscape snapshot together with ordered Evidence lineage as a plain mapping. The Adapter performs representation only; it does not determine continuity, semantic equivalence, historical identity, or domain meaning.

## Non-goals

- persistence semantics
- backend-specific storage behavior
- semantic interpretation
- continuity scoring or claims
- migration
- replay semantics
- new Kernel or Evidence schema

## Result

`LandscapeState → Adapter → external observation representation` is now directly testable. Semantic interpretation remains outside the Runtime Kernel.

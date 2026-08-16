# R0010 Projection Boundary Implementation

Implemented on branch `r0010/projection-boundary`.

The change introduces a minimal boundary between immutable Evidence and mutable Landscape State:

```text
Observation
    ↓
Evidence
    ↓
Projection
    ↓
Landscape State
```

`LandscapeState.apply_evidence()` remains as a compatibility boundary, but now delegates through `project_evidence()` rather than mutating state from Evidence directly.

Projection history is retained so later projections do not erase the provenance of earlier state changes.

Verification is covered by `runtime/test_projection.py`.

The implementation deliberately does not introduce new Foundation theory, domain semantics, or a new Evidence identity model.

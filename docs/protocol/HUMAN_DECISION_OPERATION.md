# Human Decision / Operation Boundary

## MVP status

Draft v0.1 — explicit human authorization boundary.

## Flow

```
Simulation
    ↓
Human Decision
    ↓
Operation
    ↓
Reality
    ↓
Evidence / AIwitness
```

## Rules

1. Simulation cannot authorize itself.
2. An Operation requires an explicit approved HumanDecision.
3. HumanDecision is linked to the Simulation it evaluates.
4. Operation results are observable.
5. Reality change is reported explicitly by the Operation result.
6. Operation failure is observable and does not become a successful action.

This keeps the decision boundary outside the AI simulation layer.

## Reconstruction

A future AIwitness record can link:

- Simulation ID
- Human Decision ID
- decision status / actor
- Operation ID
- operation status
- reality_changed
- resulting Evidence reference

The external adapter remains responsible for actual domain-side execution.

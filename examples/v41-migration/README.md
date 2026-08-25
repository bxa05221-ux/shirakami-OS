# v4.1 Migration Example

This directory is reserved for a compatibility example showing how the Shirakami Model v4.1 prototype can be expressed through the current Shirakami OS boundaries.

The original v4.1 implementation remains a historical prototype. It is not copied into Runtime as-is.

## Boundary

```text
v4.1 input
   ↓
Context Snapshot
   ↓
Protocol request
   ↓
Runtime
   ↓
Model Adapter
   ↓
External AI
   ↓
Proposal / Observation
   ↓
Validation
   ↓
Transition
   ↓
Evidence
```

## Important distinction

A model response such as `adopted_judgment: 暗問層` is an interpretation produced by the processing path. It is not automatically a Landscape state transition.

The migration therefore preserves the distinction between:

- observation;
- interpretation/proposal;
- decision/eligibility;
- transition;
- evidence;
- resulting Landscape state.

This example does not redefine any protocol semantics. It only establishes the implementation boundary needed to migrate the existing prototype safely.

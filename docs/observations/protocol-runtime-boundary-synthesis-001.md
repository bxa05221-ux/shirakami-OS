# Protocol / Runtime Boundary Synthesis 001

## Status

Observation synthesis. No architecture refactor is authorized by this document.

## Scope

This document consolidates the recent boundary observations around Protocol, Runtime, Evidence, and Landscape.

## Observed Path

```text
Protocol Definition
      ↓
Protocol IR
      ↓
Protocol Bridge
      ↓
Transition
      ↓
Runtime Execution
      ↓
ExecutionResult
      ↓
Evidence
      ↓
Landscape State
```

## Observed Facts

1. Existing Protocol specimens with different semantic density can pass through the same generic bridge path.
2. The current bridge does not implement domain-specific branches for symbolic, manga, or quickstart semantics.
3. Runtime validation observed so far is execution-contract validation: identifier validity, callable/executable shape, input shape, Transition result shape, budget/error handling.
4. Evidence records execution outcomes without becoming a semantic interpreter.
5. Landscape currently applies transition evidence using a minimal changed-state gate rather than domain-specific semantic interpretation.
6. No existing specimen has yet demonstrated a necessary semantic-selection step that cannot be represented by the current generic Transition boundary.
7. No existing specimen has yet demonstrated a necessary backend-neutral TransitionPlan as a distinct intermediate representation.

## Current Boundary Model

The evidence currently supports the following model:

```text
Protocol declares meaning
        ↓
Transition carries the declared execution unit
        ↓
Runtime enforces execution contract
        ↓
Evidence preserves the observed result
        ↓
Landscape reflects the resulting state
```

## Unresolved Hypotheses

The following remain open rather than normative:

- A distinct Protocol Interpreter may become necessary if semantic eligibility, verification, or transition selection appears.
- A TransitionPlan may become necessary if multiple Protocol-level decisions must be materialized before mechanical execution.
- Landscape projection may require stronger eligibility or schema validation when richer state semantics emerge.

## Architecture Decision at This Observation Point

Do not add an Interpreter or TransitionPlan yet.

Do not rewrite the Runtime merely to make the architecture symmetrical.

Keep the current generic Transition boundary while collecting evidence from new Protocols and failure cases.

## Freeze Candidates

The following can be treated as provisional boundaries for β0.1:

- Protocol describes/declares behavior.
- Transition is the current Protocol/Runtime handoff.
- Runtime owns execution-contract enforcement.
- Evidence records observed execution outcomes.
- Landscape consumes evidence to represent observable state.

These are provisional and may be revised only by subsequent observation.

## Next Observation Target

The next useful test is not another semantic Protocol specimen. It is a case that forces a choice or rejection before execution, such as:

- eligibility failure;
- verification failure;
- competing transitions;
- Landscape-dependent transition selection;
- invalid or conflicting evidence.

The purpose is to determine whether a genuine semantic authority boundary emerges.

## Principle

Do not create an architectural layer because the abstraction is attractive.
Create it only when observed behavior requires a distinct responsibility.

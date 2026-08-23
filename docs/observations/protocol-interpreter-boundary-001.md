# Protocol Interpreter Boundary Observation 001

## Status

Design hypothesis under observation. No Runtime refactor is authorized by this document.

## Source Observation

External review proposed a three-part boundary:

```text
Protocol Definition
        ↓
Protocol Interpreter
        ↓
Runtime Executor
```

The current implementation already separates Matome/Protocol IR loading from the Runtime-facing bridge. `runtime/protocol_bridge.py` converts validated `ProtocolIR` into a Runtime-compatible callable while explicitly avoiding domain-specific action branches.

The current Runtime prototype performs execution-contract validation, invokes a Protocol callable, and returns an observable `Transition` inside an `ExecutionResult`.

## Current Boundary

```text
Matome YAML
    ↓
Protocol Loader
    ↓
Protocol IR
    ↓
Protocol Bridge
    ↓
Runtime
    ↓
ExecutionResult / Transition
    ↓
Evidence
    ↓
Landscape State
```

## Hypothesis

A distinct `Protocol Interpreter` / `TransitionPlan` boundary may be useful if existing Protocols demonstrate a stable semantic-selection responsibility that is neither Protocol Definition nor mechanical Runtime execution.

This must be demonstrated by existing Protocols before the boundary is promoted to a normative contract.

## Important Distinction

Runtime validation such as:

- execution budget validity;
- protocol identifier shape;
- callable/executable object validity;
- input container validity;
- Transition result type;
- execution exception handling;

is currently treated as **Execution Contract Validation**, not as semantic authority.

Semantic authority would instead include questions such as:

- Is this Protocol eligible for the current Landscape?
- Which declared transition is selected?
- What semantic preconditions are satisfied?
- What meaning-bearing effect is requested?

## Boundary Test

Before introducing `TransitionPlan`, compare at least two existing Protocols and ask:

1. Does Protocol meaning require a selection decision not expressible as data?
2. Is that selection independent of Evidence creation?
3. Can the selected operation be represented as a backend-neutral execution plan?
4. Can Runtime execute that plan without understanding its domain meaning?
5. Does the same plan shape recur across multiple Protocols?

If the answer to these questions is consistently yes, an Interpreter Contract becomes a candidate for RFC/specification.

If not, retain the current bridge and do not introduce an abstraction merely because it is architecturally attractive.

## Non-Goals

This observation does not authorize:

- a Runtime rewrite;
- creation of a universal semantic engine;
- moving Evidence responsibility into an Interpreter;
- moving Adapter calls into an Interpreter;
- introducing `TransitionPlan` solely for architectural symmetry.

## Current Conclusion

The three-way split is a **candidate architectural hypothesis**, not yet a Shirakami OS contract.

The next valid action is observation of existing Protocols and tests, followed by evidence-backed boundary refinement.

# Runtime Replacement Full Round Trip

## MVP v0.1

This protocol verifies the complete external lifecycle for two replaceable
Runtime implementations.

Both Runtime A and Runtime B receive the same PromptSpec and independently
proceed through:

Simulation -> AIwitness -> Human Decision -> Operation -> resulting Evidence
-> Reconstruction.

## Invariants

The following external meaning remains stable:

- Prompt ID
- Protocol ID
- Context version
- input Evidence references
- Human approval requirement
- Operation boundary

Runtime-specific provenance remains distinct:

- Simulation ID
- AIwitness ID
- Human Decision ID
- Operation ID
- resulting Evidence references
- simulation output

This distinction is intentional. Replacement must preserve the trace structure,
not erase the fact that a different Runtime was used.

## Architectural result

The tested lifecycle is:

Evidence
-> Context
-> Matrix
-> Protocol
-> Prompt
-> Runtime A or Runtime B
-> Simulation
-> AIwitness
-> Human Decision
-> Operation
-> resulting Evidence
-> Reconstruction

The same external state can therefore pass through different Runtime
implementations while retaining an independently reconstructable lifecycle.

## Non-goals

This MVP does not compare the quality or correctness of Runtime A and Runtime B.
It does not assert that the resulting operations were substantively correct.
It verifies only that Runtime substitution does not break the Shirakami
trace and human-decision boundary.

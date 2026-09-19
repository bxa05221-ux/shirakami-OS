# Runtime Replacement Protocol

## MVP v0.1

This protocol verifies that a Shirakami Runtime can be replaced without
changing the external Context, Evidence, Protocol, or Prompt boundary.

The Runtime is an implementation detail. The traceable meaning of the
interaction remains outside the Runtime.

## Verification

Two deterministic Runtime implementations receive the same PromptSpec.

- Runtime A produces one simulation output.
- Runtime B produces a different simulation output.
- Both preserve the same Prompt ID, Protocol ID, Context version, Evidence
  references, and uncertainty boundary carried by the Prompt.

A replacement therefore changes the simulation result, but does not require
rewriting the external state or protocol identity.

## Boundary

This MVP does not claim that two AI systems are equivalent or that their
outputs are equally correct. It verifies only structural substitutability at
the Shirakami Runtime boundary.

The intended chain is:

Evidence -> Context -> Matrix -> Protocol -> Prompt
-> Runtime A or Runtime B -> Simulation -> AIwitness
-> Human Decision -> Operation -> resulting Evidence

## Design implication

Shirakami does not need to make one AI permanent.

The durable object is the relationship between Reality, Evidence, Context,
Protocol, Human Decision, and trace reconstruction.

AI can be replaced while that relationship remains addressable.

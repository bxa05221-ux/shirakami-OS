# Full Trace MVP

Status: MVP v0.1

## Executable path

The first end-to-end path is now represented by a single test:

Evidence
→ Context
→ 3D Matrix state
→ Protocol routing
→ Prompt assembly
→ Simulation
→ AIwitness
→ Human Decision
→ Operation
→ resulting Evidence

The test intentionally uses a provider-independent simulation callable.

## What this proves

The MVP can preserve the identity of one execution chain across each boundary.

The chain retains:

- input Evidence references
- Context version
- Matrix-derived routing
- selected Protocol
- Prompt identifier
- Simulation identifier
- AIwitness identifier
- Human Decision identifier
- Operation identifier
- resulting Evidence references

## What this does not prove

This is not proof that an external AI provider is safe, correct, or reliable.

It does not:

- invoke a provider-specific model
- determine whether a human decision was substantively correct
- guarantee that external Reality was recorded completely
- replace domain-specific Evidence systems
- authorize an Operation without an explicit HumanDecision

## Verification target

If the same explicit Context, Protocol registry, and deterministic simulation are supplied, the trace identifiers and boundary relationships can be reproduced.

The next verification layer is therefore not another abstraction. It is execution against the actual repository test suite and, later, against external Adapters.

# AIwitness Runtime A/B Comparison

## MVP v0.1

This protocol verifies that Runtime replacement remains observable through
AIwitness while the external Shirakami meaning boundary stays stable.

Runtime A and Runtime B receive the same PromptSpec. Their simulation outputs
are intentionally different. AIwitness records both results without treating
them as equivalent.

## Invariants

Across the two witnesses, the following remain identical:

- Prompt ID
- Protocol ID
- Context version
- input Evidence references
- uncertainty boundary

The following remain different and therefore observable:

- Simulation ID
- Runtime-specific simulation output

## Interpretation

This is not an accuracy comparison between AI systems.

It verifies a stronger architectural property: changing the Runtime does not
require changing the external Context, Evidence, Protocol, or Prompt identity.

The difference in AI output remains part of the trace rather than being
normalized away.

## Trace

Context / Evidence
-> Protocol
-> Prompt
-> Runtime A or Runtime B
-> Simulation
-> AIwitness
-> Human Decision

The same external state can therefore be evaluated through different Runtime
implementations without losing provenance.

## Non-goals

This MVP does not establish that Runtime A or Runtime B is safer, smarter,
more accurate, or preferable. It only establishes structural traceability and
replacement visibility.

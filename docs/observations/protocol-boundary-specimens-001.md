# Protocol Boundary Specimens Observation 001

## Status

Observed. No architectural refactor authorized.

## Purpose

Compare existing Protocol specimens at opposite ends of the semantic spectrum to determine whether a distinct Protocol Interpreter / TransitionPlan boundary is required.

## Specimen A — Quickstart Observation Protocol

`examples/quickstart/protocol.yaml` is intentionally mechanical. Its pipeline declares observe → transition → evidence → landscape actions: `capture_input`, `mark_observed`, `capture_evidence`, and `expose_state`.

The existing β0.1 integration path can carry this structure through Runtime, Evidence, and Landscape without requiring domain-specific action branches in the bridge.

## Specimen B — Symbolic Recurrence Boundary Test

`protocols/manual/symbolic-recurrence-boundary.yaml` is semantically dense. It declares preservation of symbolic lineage, carrying symbolic references as protocol data, exposing recurrence as an observable transition, and preserving recurrence lineage.

The current generic bridge still does not execute those action names as domain operations. It preserves the pipeline as Protocol data inside a generic `matome.protocol.transition`.

This is significant: the current Runtime vertical slice demonstrates transport and observability of semantic declarations, not semantic execution of those declarations.

## Specimen C — Manga User Manual Protocol

`protocols/manual/manga-user-manual.yaml` sits between the two. It contains an experimental rendering intent, an observe/evidence pipeline, and a substantial manual data structure including multilingual pages. The existing vertical-slice test verifies that its Protocol identity, version, input, transition, Evidence, and Landscape projection survive the path.

## Boundary Result

The three specimens do **not** yet demonstrate a recurring need for a `TransitionPlan`.

What they demonstrate is:

```text
Protocol Definition
      ↓
validated Protocol IR
      ↓
Generic bridge
      ↓
mechanical Runtime transition
      ↓
Evidence
      ↓
Landscape projection
```

The semantic action names remain data. No stable cross-Protocol semantic selection mechanism has yet appeared that would require a separate Interpreter contract.

## Important Finding

The strongest current boundary is not yet:

```text
Definition → Interpreter → Executor
```

It is:

```text
Definition / IR
      ↓
Interpretation candidate (currently generic bridge)
      ↓
Execution Contract Validation
      ↓
Runtime transition
```

The word `candidate` is deliberate. Naming the bridge an Interpreter would currently imply more semantic authority than the implementation demonstrates.

## Consequence

Do **not** introduce `TransitionPlan` or refactor Runtime β0.1 solely on the basis of the three-layer proposal.

The next useful observation would require a Protocol whose declared pipeline contains an actual choice or eligibility condition that cannot be represented as passive Protocol data. Such a specimen would test whether semantic selection is a real cross-Protocol responsibility.

## Conclusion

The Copilot three-layer proposal remains a useful hypothesis. The current specimens provide evidence for a distinction between semantic declarations and mechanical execution, but not yet enough evidence for a new normative Interpreter/TransitionPlan layer.

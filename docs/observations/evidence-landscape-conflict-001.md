# Evidence → Landscape Conflict Observation 001

## Status

Stress-test result. No conflict-resolution mechanism is introduced by this observation.

## Test

Given the current β0.1 Landscape implementation, apply two valid transition Evidence records sequentially where both claim `changed: true` but assign different values to the same Landscape key.

Example:

```text
Evidence A: { changed: true, phase: "A" }
Evidence B: { changed: true, phase: "B" }
```

## Observed behavior

`EvidenceRecord` is immutable and classifies transition evidence using a non-empty transition kind plus `transition_data["changed"]`. fileciteturn126file0

`LandscapeState.apply_evidence()` accepts any Evidence record passing that predicate and applies `transition_data` with a dictionary update. There is no provenance comparison, version check, conflict detection, merge rule, or rejection path at this boundary. fileciteturn125file0

Therefore, when two valid transition Evidence records target the same key, the later application wins.

## Interpretation

This is not currently evidence that the Runtime needs an Interpreter.

It is evidence that **Landscape projection semantics are intentionally minimal in β0.1** and that conflict policy is currently unspecified.

The missing responsibility is not semantic Protocol interpretation. It is a potential **Evidence Projection / Conflict Policy** responsibility.

## Boundary question

The unresolved question is:

> Who decides whether two individually valid Evidence records are mutually compatible when projected onto the same Landscape?

Possible future answers include:

- Landscape owns conflict policy;
- a separate projection/merge layer owns it;
- Evidence carries enough causal/version metadata to make conflicts mechanically detectable;
- the current last-write-wins behavior remains the contract.

No choice is made here.

## Architectural consequence

Do not add a ConflictResolver merely because the conflict can be demonstrated.

First determine whether Shirakami OS requires conflict semantics at all, and whether those semantics are domain-neutral.

## Next observation

Test whether the existing `changed` flag is sufficient for the intended Landscape model, or whether Evidence needs causal/version/identity metadata before conflict policy can be meaningfully defined.

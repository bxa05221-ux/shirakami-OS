# Runtime Specification Gap Observation 001

## Status

Observed implementation gap. No code change is implied by this record.

## Observation

The normative Protocol Specification defines an authoring and execution path:

```text
Matome YAML
  ↓
Protocol Loader
  ↓
Protocol IR
  ↓
Runtime
```

The current Runtime β0.1 vertical slice instead accepts a Python callable directly:

```text
Python Protocol callable
  ↓
Runtime.execute()
  ↓
Transition
  ↓
ExecutionResult
```

The current implementation therefore demonstrates the Runtime execution boundary, but does not yet demonstrate the complete Matome YAML → Loader → Protocol IR → Runtime path described by the Protocol Specification.

## Evidence

`runtime/prototype.py` defines `Protocol = Callable[[ExecutionContext], Transition]` and `Runtime.execute()` accepts that callable directly.

`runtime/evidence.py` provides an immutable `EvidenceRecord` derived from `ExecutionResult`.

`runtime/landscape.py` provides `LandscapeState.apply_evidence()` for transition evidence.

## Interpretation

This is an **implementation maturity gap**, not evidence that the specification is invalid.

The current vertical slice proves a smaller boundary:

```text
Protocol callable
  ↓
Runtime
  ↓
Observable Transition
  ↓
Evidence object
  ↓
Landscape State component
```

The complete specification path remains to be verified or implemented.

## Important Non-Conclusion

Do not state that Matome YAML execution is implemented merely because the Protocol Specification defines it.

Do not state that Evidence and Landscape are fully integrated merely because the corresponding Runtime components exist.

## Next Verification Target

Determine whether a loader / Protocol IR implementation already exists elsewhere in the repository. If it does, verify whether it is connected to `Runtime.execute()`. If it does not, treat the Loader/IR boundary as an explicit implementation task rather than silently filling the gap.

## Observation Principle

The specification describes the intended contract. The Runtime demonstrates the currently executable boundary. The difference between them is itself part of the Landscape and should remain observable until resolved.

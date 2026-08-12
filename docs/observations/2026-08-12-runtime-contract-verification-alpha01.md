# Runtime Contract Verification α0.1

## Status

Verification pass performed against the current Runtime β0.1 implementation after Protocol Specification α0.1 and Adapter Contract α0.1 were introduced.

This document records implementation observations. It does not introduce new architecture.

## 1. Protocol Boundary

**Status: GAP — intentionally scoped subset**

`runtime/protocol_loader.py` implements a small, explicit Matome YAML subset. It validates `matome.title`, `matome.version`, `matome.statement`, and a non-empty `pipeline`, then produces `ProtocolIR`.

The implementation explicitly states that it does not implement the full YAML specification. This is consistent with the current β0.1 scope, but it means the Protocol Specification α0.1 is not yet a complete implementation of arbitrary Matome YAML.

Action: keep the subset explicit; do not expand the loader without an observed requirement.

## 2. Runtime Execution Boundary

**Status: PASS for the current vertical slice**

`runtime/prototype.py` provides a bounded execution context, validates the execution input, executes a supplied Protocol callable, returns an observable `Transition`, and exposes an `ExecutionResult`.

The implementation also keeps the Runtime replaceable and backend-independent at this layer.

Observation: the current Runtime executes a callable Protocol rather than directly executing `ProtocolIR`. Therefore the Protocol Loader → Runtime bridge is not yet a complete end-to-end contract.

Action: record this as the next integration gap rather than adding speculative architecture.

## 3. Evidence Boundary

**Status: PASS for the current execution boundary**

`runtime/evidence.py` converts an `ExecutionResult` into an immutable `EvidenceRecord`. Transition data is wrapped in `MappingProxyType`, and the record itself is frozen.

The updated evidence tests now match the actual Runtime failure transition (`execution.failed`) and verify that failed execution is observable without being classified as transition evidence.

## 4. Adapter Boundary

**Status: PASS for the minimum read boundary**

`runtime/adapter.py` defines a backend-agnostic `Adapter` Protocol with `read(reference)` and a deterministic `MemoryAdapter` for boundary verification.

The current implementation does not provide a generic write or read-back interface. This is acceptable for the current minimum read boundary, but it is not yet a full implementation of every optional operation described by Adapter Contract α0.1.

The GitHub-specific implementation remains outside this generic boundary.

## 5. Automated Verification

The Runtime β0.1 GitHub Actions workflow now runs the Runtime test suite before the manga-render smoke tests.

The workflow therefore verifies:

- Protocol loader behavior;
- Runtime execution and failure paths;
- Adapter boundary behavior;
- Evidence immutability and failure handling;
- Manga renderer compilation;
- Japanese and English manual rendering.

The repository must use the resulting GitHub Actions run as the authoritative execution result for this commit.

## 6. Verification Result

The current implementation is **not yet a complete implementation of Protocol Specification α0.1**.

It is a valid β0.1 minimal vertical slice with two concrete gaps:

1. ProtocolIR is produced by the Loader but is not yet the direct Runtime execution input.
2. The generic Adapter boundary currently verifies read access only; controlled write/read-back remains Backend-specific or future scope.

Neither gap requires new architecture at this stage.

## 7. Next Transition

The next implementation target should be the smallest possible bridge:

```text
Matome YAML
    ↓
Protocol Loader
    ↓
Protocol IR
    ↓
Runtime
    ↓
ExecutionResult
    ↓
Evidence
```

Only after this path is tested end-to-end should API α0.1 be considered.

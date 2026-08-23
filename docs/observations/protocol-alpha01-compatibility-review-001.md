# Protocol α0.1 Compatibility Review 001

## Status

Observed compatibility review. No implementation change implied.

## Scope

Compare the normative Protocol Specification α0.1 with the current β0.1 implementation and existing Matome Protocol artifacts.

## Verified

### 1. Authoring path

The repository contains a Matome YAML authoring path and a dependency-free β0.1 loader. `runtime/protocol_loader.py` parses the supported subset into a frozen `ProtocolIR` containing protocol identity, title, version, statement, and pipeline. The loader explicitly states that it implements only the β0.1 Quickstart subset.

### 2. Runtime path

`runtime/vertical_slice.py` composes the path:

```text
Matome YAML
  ↓
ProtocolIR
  ↓
Runtime
  ↓
ExecutionResult
  ↓
Evidence
  ↓
Projection / Landscape
```

The integration test `runtime/test_vertical_slice.py` verifies a concrete Matome Protocol through execution, Evidence, and Landscape projection.

### 3. Existing Protocol artifacts

`protocols/manual/manga-user-manual.yaml` is compatible with the loader's minimum structure and is used by the vertical-slice integration test.

`protocols/manual/symbolic-recurrence-boundary.yaml` also uses the same minimum Matome structure and carries domain-specific pipeline actions.

## Important Boundary Finding

The current bridge does **not execute the semantic meaning of individual pipeline actions**.

`runtime/protocol_bridge.py` deliberately converts the entire validated IR into one generic transition:

```text
kind = matome.protocol.transition
```

The pipeline is carried as transition data. The bridge does not dispatch `observe`, `recurrence`, `transition`, `evidence`, or action names such as `preserve_symbolic_lineage` as Runtime behaviors.

Therefore the current β0.1 implementation proves:

> **Protocol structure can be loaded, transported through Runtime, observed as a generic transition, captured as Evidence, and projected into Landscape.**

It does **not** prove:

> **Protocol-defined domain actions are semantically executed by the Runtime.**

## Compatibility Classification

| Specification requirement | Observation |
|---|---|
| Accept supported Matome subset | Verified |
| Produce Protocol IR | Verified |
| Preserve declared metadata and pipeline | Verified |
| Execute a supported Runtime transition | Verified at generic transition level |
| Preserve Evidence | Verified by vertical-slice test |
| Project resulting Landscape representation | Verified by vertical-slice test |
| Execute arbitrary Protocol action semantics | Not claimed / not implemented |
| Universal Protocol language | Explicitly out of scope |

## Interpretation

This is not a defect in β0.1. The bridge intentionally avoids inventing domain semantics. The current implementation establishes a **structural Protocol contract**, not a universal semantic execution engine.

This distinction is important for Landscape First architecture: domain meaning remains outside the Runtime Kernel unless a future specification explicitly promotes a semantic operation into the Kernel contract.

## Next Question

The next Protocol review should determine whether any existing Shirakami Protocol requires semantic dispatch inside the Kernel, or whether domain-specific actions should remain handled by Protocol-specific adapters/services outside the Kernel.

Do not expand the Protocol Specification merely because a richer Protocol exists. First identify the smallest cross-Protocol semantic requirement that is actually evidenced by multiple implementations.

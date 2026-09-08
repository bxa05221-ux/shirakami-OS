# Shirakami OS — Repository Classification

## Purpose

This document classifies repository artifacts by implementation responsibility. It does not change Shirakami theory, Protocol semantics, or the normative specification.

The purpose is to keep implementation, verification, evidence, application artifacts, and historical material distinguishable as the repository moves from Alpha toward Beta operation.

## Classification Model

```text
A. Normative / Contract Boundary
   ↓
B. Runtime / Implementation
   ↓
C. Verification
   ↓
D. Evidence / Observation
   ↓
E. Application / Product
   ↓
F. Historical / Archive
```

Classification is about repository role, not chronological age.

## A. Normative / Contract Boundary

### Primary locations

- `spec/`
- `protocols/`
- `docs/architecture/` when a document explicitly describes implementation architecture rather than normative semantics
- external `shirakami-specification` repository for stable normative contracts

### Rule

The `shirakami-OS` repository must not silently become the authoritative home of stable normative specification. Implementation-side documents may describe how the current implementation behaves, but presence in this repository does not make a document normative.

## B. Runtime / Implementation

### Primary locations

- `runtime/`
- `api/`
- `plugins/`
- `src/`
- selected executable entry points and compatibility modules

### Rule

These artifacts implement or expose the current Runtime boundary. Multiple historical or compatibility modules may coexist until their roles are explicitly classified.

Do not delete or consolidate modules solely because their names overlap.

## C. Verification

### Primary locations

- `tests/`
- experiment-specific runtime tests
- `.github/workflows/`
- `ci/`
- `experiments/`

### Rule

Verification artifacts establish observable implementation behavior. A test file or workflow existing is not evidence that the corresponding experiment succeeded. Success must be established from an observed run or other explicit verification record.

Historical experiment tests remain valuable evidence and should not be removed merely because newer experiments supersede their operational purpose.

## D. Evidence / Observation

### Primary locations

- `docs/observations/`
- immutable Evidence produced by Runtime execution

### Rule

Observation records preserve experiment boundaries, results, and non-goals. They must not be rewritten to reconcile later interpretations.

Contradictory or superseded observations remain historical evidence unless a new experiment explicitly tests the issue again.

## E. Application / Product

### Primary locations

- `apps/`
- `products/`
- `examples/`
- user-facing manuals and renderer artifacts
- `community/` where material is operational/community-facing rather than normative

### Rule

Application and product artifacts demonstrate or consume the Runtime. They must not be treated as proof of Kernel semantics unless supported by explicit tests and observations.

The current public service artifact remains a product-layer concern, separate from the Runtime Kernel.

## F. Historical / Archive

### Candidates

- obsolete implementations retained for provenance
- abandoned experiments
- superseded RFC drafts
- historical notes
- duplicate or superseded artifacts that are intentionally preserved for traceability

### Rule

Historical status must be explicit before deletion or movement. Age alone is not sufficient reason to archive or remove an artifact.

## Current Classification of Key Repository Areas

| Area | Primary role | Current handling |
| --- | --- | --- |
| `runtime/` | Runtime / Implementation | Active |
| `api/` | Runtime / API boundary | Active |
| `plugins/` | Adapter / Plugin implementation | Active |
| `tests/` | Verification | Active + historical tests |
| `.github/workflows/` | Verification / CI | Active + experiment history |
| `ci/` | Verification support | Active / classify incrementally |
| `docs/observations/` | Evidence / Observation | Immutable history |
| `docs/architecture/` | Architecture / implementation guidance | Active; not automatically normative |
| `docs/rfc/` | Design / RFC history | Active drafts + historical promoted RFCs |
| `spec/` | Implementation-side specification boundary | Active; normative authority remains external |
| `protocols/` | Protocol source artifacts | Active; classify per artifact |
| `apps/` | Application | Active |
| `products/` | Product / service artifacts | Active |
| `examples/` | Examples / executable demonstrations | Active |
| `community/` | Community-facing material | Active; classify per artifact |
| `experiments/` | Experiment support/history | Active + historical |
| `src/` | Implementation source | Active; classify modules before refactoring |

## Runtime Module Classification Rule

The Runtime directory currently contains modules with overlapping or historical naming patterns, including compatibility and bridge components.

Before any consolidation, each module should be assigned one of:

```text
KERNEL
COMPATIBILITY
ADAPTER
API
EXPERIMENT
HISTORICAL
UNKNOWN
```

`UNKNOWN` is an acceptable temporary state. It is preferable to an inferred classification.

## Evidence Integrity Rule

Repository organization must never alter the meaning of existing Evidence.

```text
Artifact exists
    ≠
Experiment succeeded

Current implementation
    ≠
Historical implementation

Landscape snapshot
    ≠
Evidence lineage

External AI observation
    ≠
Truth authority
```

## Migration Rule

Repository reorganization should proceed in this order:

1. classify
2. verify references
3. document intended movement
4. move only when necessary
5. run the affected verification
6. preserve provenance

No broad directory migration is authorized by this document.

## Next Boundary

After repository classification, define the canonical CI checks for `main`. Only those checks should later be candidates for required branch protection.

The next implementation step is therefore:

```text
Repository Classification
        ↓
Canonical CI Selection
        ↓
Main Protection Design
        ↓
R0053 Temporal Evidence Addressability
```

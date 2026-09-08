# Shirakami OS — Canonical CI

## Purpose

Define the single canonical CI check candidate for `main` branch protection.

This document is implementation/operations guidance. It does not change Shirakami theory, Protocol semantics, or Evidence meaning.

## Canonical Workflow

Workflow:

```text
Runtime β0.1 Verification
```

Path:

```text
.github/workflows/runtime-beta-0.1.yml
```

Canonical job/check:

```text
test-runtime
```

The workflow name and the GitHub Actions check-run/job name are distinct. Branch protection must target the actual required check name (`test-runtime`), not assume that the workflow display name is the status-check context.

## Verification Scope

The canonical job currently performs:

1. Runtime and boundary tests:
   `python -m pytest runtime tests -q`
2. Manga renderer compilation:
   `python -m py_compile runtime/manga_manual.py`
3. Japanese smoke render
4. English smoke render

This makes it the appropriate Kernel/Runtime boundary verification candidate currently available in the repository.

## Non-Canonical Workflows

The repository also contains:

- experiment-specific workflows (`R00xx`)
- specialized Runtime workflows such as OPPAI Runtime
- specialized AATS Thread Wayfinding workflows

These workflows remain valuable verification/evidence infrastructure, but they are not candidates for the single required `main` protection check merely because they exist or because a historical experiment used them.

## Selection Rule

```text
Canonical CI
    =
current Runtime boundary verification

Experiment workflow
    ≠
required main protection check
```

A workflow becomes a branch-protection candidate only after its role has been explicitly classified and its current verification scope has been confirmed.

## Careless-Mistake Guard

Before applying branch protection, verify all of the following against the live repository:

- workflow file exists at the documented path
- workflow display name is `Runtime β0.1 Verification`
- job/check name is `test-runtime`
- the job completes successfully on the target commit
- the required check name is selected from the observed check-run, not inferred from the workflow name
- experiment-specific failures are not accidentally made required
- no semantic approval is inferred from CI success

## Current Boundary

```text
Repository Classification
        ↓
Canonical CI Selection  ← this document
        ↓
Main Protection Design
        ↓
R0055 formal handoff
```

R0055 remains blocked until a formal research-side 的目yaml handoff exists.

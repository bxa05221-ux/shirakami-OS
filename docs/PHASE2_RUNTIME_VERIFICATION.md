# Shirakami OS — Phase 2 Runtime Verification

## Status

**Phase 2: Complete**

Phase 2 moved the project from **understanding** to **trying and verifying** the existing Runtime and API boundaries.

The goal was reproducibility, not feature expansion.

## Verification targets

A third party should be able to:

1. obtain the repository from a clean checkout;
2. run the dependency-free Quickstart;
3. observe a Runtime execution;
4. inspect Evidence and Landscape State output;
5. run the API test suite through CI;
6. distinguish demonstrated behavior from experimental or unverified behavior.

## Current executable path

The repository contains a dependency-free Quickstart:

```text
Matome YAML
    ↓
Protocol IR
    ↓
Protocol Bridge
    ↓
Runtime
    ↓
Evidence
    ↓
Landscape State
    ↓
SUCCESS
```

`examples/quickstart/run.py` requires no GitHub credentials or external packages and exits non-zero when the Runtime result is not completed.

The Quickstart CI now executes this path automatically.

## API verification

The existing `Shirakami API CI` workflow has successfully executed the API test job on the v4.1 migration branch.

The successful job includes:

```text
Checkout
Set up Python
Install dependencies
Run API tests
```

This establishes that the API test boundary is executable in GitHub Actions.

## Runtime verification

The Runtime verification workflow now passes the complete Runtime test and smoke-render path.

The verified steps are:

```text
Runtime unit tests        PASS
Manga renderer compile    PASS
Japanese smoke render     PASS
English smoke render      PASS
```

The final successful Runtime verification run reported **46 passed tests**.

During verification, three implementation-boundary defects were found and corrected:

1. direct-module vs package imports in the Quickstart / Runtime bridge;
2. Runtime test import-path configuration in CI;
3. SVG text wrapping assumptions in the English manual test.

These were implementation/test-boundary corrections. No new Protocol semantics were introduced to make the Runtime pass.

## Quickstart CI

Phase 2 adds a dedicated GitHub Actions workflow:

`.github/workflows/quickstart-ci.yml`

It executes:

```bash
python examples/quickstart/run.py
```

on Ubuntu with Python 3.11.

This turns the Quickstart from documentation-only guidance into a continuously checked reproducibility path.

## Exit criteria

All Phase 2 criteria are now demonstrated:

- [x] dependency-free Quickstart exists;
- [x] Quickstart has an explicit success/failure exit condition;
- [x] API test CI exists and has passed;
- [x] Quickstart CI exists;
- [x] Quickstart CI passes;
- [x] Runtime unit tests pass;
- [x] Runtime smoke-render checks pass;
- [x] reviewer can follow the documented path from README to execution evidence;
- [x] no new Protocol semantics were introduced merely to make the Runtime pass.

## What Phase 2 does not claim

Phase 2 does not establish:

- production readiness;
- API stability;
- authentication or billing contracts;
- complete execution support for all Shirakami Protocols;
- external architectural validation;
- or completion of Shirakami OS.

Those remain later-phase concerns.

## Next gate

The project should now move to **Phase 3 — Review / Evaluate** rather than immediately adding more Runtime features.

The review target is the existing boundary:

**Landscape → Evidence → Specification / Protocol → Runtime → Adapter → Execution → Observation**

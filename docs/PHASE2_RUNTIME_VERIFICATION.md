# Shirakami OS — Phase 2 Runtime Verification

## Status

**Phase 2: Verification in progress**

Phase 2 moves the project from **understanding** to **trying and verifying** the existing Runtime and API boundaries.

The goal is reproducibility, not feature expansion.

## Verification targets

A third party should be able to:

1. obtain the repository from a clean checkout;
2. run the dependency-free Quickstart;
3. observe a Runtime execution;
4. inspect Evidence and Landscape State output;
5. run the API test suite through CI;
6. distinguish demonstrated behavior from experimental or unverified behavior.

## Current executable path

The repository already contains a dependency-free Quickstart:

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

`examples/quickstart/run.py` explicitly states that it requires no GitHub credentials or external packages and exits non-zero when the Runtime result is not completed.

## API verification

The existing `Shirakami API CI` workflow has successfully executed the API test job on the v4.1 migration branch.

The successful job included:

```text
Checkout
Set up Python
Install dependencies
Run API tests
```

This establishes that the API test boundary is executable in GitHub Actions.

## Quickstart CI

Phase 2 adds a dedicated GitHub Actions workflow:

`.github/workflows/quickstart-ci.yml`

It executes:

```bash
python examples/quickstart/run.py
```

on Ubuntu with Python 3.11 for pushes to development branches and pull requests targeting `main`.

This turns the Quickstart from documentation-only guidance into a continuously checked reproducibility path.

## Exit criteria

Phase 2 can be considered complete when all of the following are demonstrated on the same reviewable branch / PR:

- [x] dependency-free Quickstart exists;
- [x] Quickstart has an explicit success/failure exit condition;
- [x] API test CI exists and has passed;
- [x] Quickstart CI exists;
- [ ] Quickstart CI passes on the Phase 2 head commit;
- [ ] reviewer can follow the documented path from README to execution evidence;
- [ ] no new Protocol semantics were introduced merely to make the Runtime pass.

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

After the Quickstart CI passes, the project should move to **Phase 3 — Review / Evaluate** rather than immediately adding more Runtime features.

The review target is the existing boundary:

**Landscape → Evidence → Specification / Protocol → Runtime → Adapter → Execution → Observation**

# R0074 — Operation Replay Boundary

Status: completed

## Purpose

Verify that repeated execution of the same `operation_id` receives a distinct execution identity without changing the operation identity itself.

## Baseline

- Protected `main`: `984bc73ee542cbd5abe03616665085fdde9359bc`
- R0073 established the GitHub Operation Execution workflow.
- Canonical verification gate: `test-runtime`

## Observation

R0073 used `operation/${OPERATION_ID}` as the branch identity and `${OPERATION_ID}-operation-execution.md` as the Artifact identity.

R0074 separates operation identity from execution identity:

- Operation ID identifies the declared operation.
- Execution ID identifies one execution instance.
- Branch identity combines both.
- Artifact identity combines both.

The GitHub workflow uses the GitHub Actions `run_id` as the execution identity.

## Boundary Rules

- Replaying an operation does not overwrite a previous execution branch.
- Replaying an operation does not overwrite a previous execution Artifact.
- Operation planning remains delegated to `plan_operation(...)`.
- No Landscape or Evidence mutation is introduced.
- No Protocol semantics or theory is introduced.
- Protected merge remains outside the workflow.

## Verification

Focused tests verify deterministic naming, distinct execution identities, safe normalization, and rejection of missing execution identity.

The R0074 implementation was merged through protected PR #173.

## Result

Completed.

- Implementation merge commit: `279f745eb4de396755b70f2c462226637b2069d4`
- Protected `main` was verified to advance to the same commit after merge.
- R0074 replay-safe execution naming is now part of the mainline operation execution path.

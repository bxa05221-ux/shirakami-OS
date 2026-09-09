# R0074 — Operation Replay Boundary

Status: implementation observation

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

Canonical `test-runtime` remains the merge gate.

## Result

Pending canonical verification and protected merge.

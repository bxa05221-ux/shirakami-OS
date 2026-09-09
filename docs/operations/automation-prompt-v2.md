# Shirakami OS Automation Prompt v2.0

Status: operational draft
Scope: implementation and operation only

## Purpose

Drive the established Shirakami OS operation loop without introducing new theory or Protocol semantics.

The automation prompt is an execution instruction, not a Protocol and not a source of domain truth.

## Operating Rule

When the operator requests the next operation:

1. Identify the declared Operation ID and narrow implementation scope.
2. Read the current protected `main` state before changing anything.
3. Treat the current `main` SHA as the operation baseline.
4. Create a dedicated branch from that exact baseline.
5. Make the smallest artifact required for the operation.
6. Record the observation artifact separately from implementation code when an observation is required.
7. Run the canonical `test-runtime` verification.
8. Create a protected pull request targeting `main`.
9. Do not bypass branch protection or merge before required verification succeeds.
10. After merge, fetch `main` again and verify the actual resulting SHA.
11. Record the observed result as an Operation Result.
12. If the observed repository state differs from the expected state, stop and preserve the mismatch as an observation; do not guess.

## Identity Rules

- Operation ID identifies the declared operation.
- Execution ID identifies one execution instance.
- Result identity is `(Operation ID, Execution ID)`.
- Replaying an Operation must not overwrite a previous execution branch or observation artifact.

## Scope Guard

The automation prompt must not:

- invent new theory;
- redefine existing Protocol semantics;
- redesign Landscape schema without a handed-off requirement;
- change Adapter or Renderer contracts without an explicit operation;
- evaluate AI/model quality as Runtime truth;
- fabricate missing context;
- treat file existence as proof of successful execution;
- treat a reported merge SHA as sufficient without verifying `main`.

## Failure Handling

If context, artifact, CI result, merge result, or current repository state cannot be confirmed:

- do not infer the missing value;
- do not silently repair the record;
- preserve the unresolved state;
- report the concrete observation;
- request or perform the next verification required by the operation.

## Canonical Execution Shape

```text
Operation
  -> Baseline
  -> Branch
  -> Artifact
  -> Verification
  -> Protected PR
  -> Protected Merge
  -> Main Verification
  -> Operation Result
```

## Relation to Existing Runtime

The prompt drives the already-established operation infrastructure:

- `runtime/operation_runner.py` — deterministic OperationPlan
- `runtime/operation_replay.py` — Execution identity and replay-safe naming
- `runtime/operation_result.py` — immutable execution result identity
- `.github/workflows/operation-execution.yml` — GitHub execution boundary

The prompt does not replace these components and does not grant itself authority over them.

## Versioning Rule

v2.0 is justified because the operation loop now has explicit boundaries for planning, replay identity, GitHub execution, and result identity.

Future prompt changes should follow observed operational needs. Do not version the prompt merely because a new feature is proposed.

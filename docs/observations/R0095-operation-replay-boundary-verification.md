# R0095 — Operation Replay Boundary Verification

## Scope

Verify that the actual Runtime execution path preserves the `(operation_id, execution_id)` identity produced by `OperationExecutor` and that the existing replay boundary derives distinct branch and Artifact addresses from that identity.

## Baseline

- main: `956bf4d35a0dd2e2860d641d1051f80bc71f3bd3`
- verification gate: `test-runtime`

## Verification

The verification test constructs a validated `OperationPlan`, binds it to an `ExecutionRequest`, executes it through `OperationExecutor`, and then derives replay addresses from the resulting `OperationResult.identity`.

The test checks:

1. Different execution IDs for the same operation produce distinct execution identities, branches, and observation Artifacts.
2. Changing only the observed outcome does not change the replay address for the same execution identity.

## R0094 follow-up observation

R0094 created a manually named execution Artifact outside the existing `runtime.operation_replay.execution_artifact()` boundary. R0095 therefore verifies the actual Runtime path rather than introducing a new replay naming mechanism.

This is an implementation-use/integration verification. It does not add Protocol semantics, alter Landscape/Evidence meaning, or claim autonomous operation.

## Expected boundary

`OperationExecutor -> OperationResult.identity -> operation_replay`.

The replay naming mechanism remains the existing Runtime implementation; this observation only verifies that the actual execution result can be used as its input without identity loss.

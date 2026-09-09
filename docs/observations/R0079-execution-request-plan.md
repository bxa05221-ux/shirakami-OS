# R0079 — Execution Request → Operation Plan

## Purpose

Connect the established input-side `ExecutionRequest` boundary to the existing deterministic `OperationPlan` boundary.

## Baseline

`51da9ae7ee9f60c0969f14a0c9098333548c1d89`

## Scope

- implementation / operation only
- validate Operation ID alignment
- reuse existing `plan_operation()` behavior

Explicitly out of scope:

- new theory
- new Protocol semantics
- Landscape/Evidence schema changes
- Adapter/Renderer contract changes
- AI/model quality evaluation
- GitHub workflow dispatch
- execution authority
- Landscape/Evidence mutation

## Boundary

`ExecutionRequest` is the input-side identity boundary.

`plan_execution_request()` checks that the request's Operation ID matches the declared operation, then delegates to the existing `plan_operation()`.

The planner does not execute the operation and does not mutate repository, Landscape, or Evidence state.

## Verification

The test verifies:

1. a matching request produces the existing deterministic operation plan;
2. an Operation ID mismatch is rejected;
3. planning does not introduce an `execute` capability on the request.

## Continuity

The established operational chain is now explicit through the planning boundary:

`Operation → ExecutionRequest → OperationPlan → Execution → OperationResult`

R0079 does not implement or claim remote execution. It only connects the established request and plan boundaries.

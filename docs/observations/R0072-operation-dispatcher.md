# R0072 — Operation Dispatcher

Status: implementation observation

## Purpose

Introduce the smallest GitHub Actions boundary for executing a validated Shirakami OperationPlan.

## Baseline

- R0071 is merged on protected `main`.
- Baseline merge SHA: `7e7399bb0dac89c0a7e4a489f9f5889ecddb6341`
- Canonical verification gate: `test-runtime`

## Observation

The dispatcher is manually invoked through GitHub Actions with three declared inputs:

- `operation_id`
- `base_ref`
- `scope`

It reconstructs the existing `OperationDefinition`, validates it through the existing `plan_operation(...)` boundary, prints the deterministic plan, and runs the canonical Runtime test suite.

## Boundary Rules

- The dispatcher does not mutate GitHub state.
- The dispatcher does not mutate Landscape or Evidence.
- The dispatcher does not create or merge Pull Requests.
- Forbidden scopes remain rejected by the existing runner boundary.
- `test-runtime` remains the canonical verification gate.
- No new Protocol semantics or theory is introduced.

## Non-goals

- Automatic branch creation
- Automatic Artifact creation
- Automatic Pull Request creation
- Automatic protected merge
- New theory
- Landscape schema redesign
- Adapter/Renderer contract changes
- AI/model quality evaluation

## Result

Pending canonical verification and protected merge.

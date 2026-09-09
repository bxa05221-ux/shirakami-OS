# R0072 — Operation Dispatcher

Status: completed

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

## Verification

- R0072 head SHA: `ad84cc01579af8d8ca0278f6a725ebee19bde46f`
- Runtime β0.1 Verification: success
- canonical `test-runtime`: success
- Runtime and boundary tests: success
- manga renderer compile: success
- Japanese/English smoke-render: success
- Protected PR #169: merged successfully
- R0072 merge SHA: `a7ef351c70c653ceb6edc1f6f826d634ceb48e48`

## Result

R0072 completed successfully. The GitHub Actions dispatcher can manually receive a declared operation, validate it through the existing Operation Runner, print the deterministic OperationPlan, and execute the canonical Runtime test suite. It remains read-only with respect to GitHub, Landscape, and Evidence and introduces no new Protocol semantics or theory.

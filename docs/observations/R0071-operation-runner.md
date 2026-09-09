# R0071 — Minimal Operation Runner Boundary

Status: implementation observation

## Purpose

Introduce the smallest executable boundary for automating the repeated operational-loop procedure without moving judgment into Runtime.

## Baseline

- R0070 closure is merged on protected `main`.
- Baseline merge SHA: `f086af8230eef1f2fce664bde28bacec0962d39c`
- Canonical verification gate: `test-runtime`

## Observation

`runtime/operation_runner.py` accepts a declarative `OperationDefinition` and produces a deterministic `OperationPlan`.

The plan records the existing operational sequence:

1. record baseline
2. create artifact
3. run `test-runtime`
4. create protected PR
5. record merge result

The runner is intentionally planning-only in this first step. It does not mutate GitHub, create branches, merge PRs, or reinterpret Protocol semantics.

## Boundary Rules

- Human/research-side judgment remains outside the runner.
- Forbidden scopes are rejected rather than inferred away.
- The canonical verification gate remains `test-runtime`.
- The runner does not modify Landscape or Evidence.
- The runner does not create new Protocol semantics or contracts.

## Scope

One minimal Runtime module, focused tests, and this observation record.

No GitHub mutation automation, new theory, Landscape schema redesign, Adapter/Renderer contract change, or AI/model quality evaluation is introduced.

## Verification

The Artifact must pass the canonical `test-runtime` gate before entering protected `main`.

## Result

Pending canonical verification and protected merge.

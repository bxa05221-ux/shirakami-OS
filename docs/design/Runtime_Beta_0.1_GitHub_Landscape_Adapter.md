# Runtime β0.1 GitHub Landscape Adapter

Status: Implementation Preparation
Version: 0.1
Date: 2026-08-11

## Purpose

Introduce GitHub as one concrete implementation of the existing Landscape Adapter boundary.

GitHub is not a Runtime dependency and does not become the definition of Landscape.

## Boundary

```text
Runtime
  ↓
Landscape Adapter
  ↓
GitHub Client
  ↓
GitHub Landscape
```

The Runtime knows only the Landscape Adapter contract.

The GitHub-specific adapter knows only the injected GitHub Client contract.

## Minimal Operations

The adapter supports:

- reading the external Landscape;
- applying a verified Landscape transition.

The first implementation intentionally does not define repository synchronization, commit policy, authentication, conflict resolution, or GitHub event semantics.

## Verification Strategy

A deterministic `FakeGitHubClient` is used first to verify the boundary without network access.

This proves that:

1. GitHub can be represented as an external Landscape implementation;
2. Runtime does not need GitHub-specific execution logic;
3. only verified transition Evidence reaches the external Landscape;
4. failure Evidence does not create a Landscape change.

A real GitHub transport can subsequently implement the same client contract.

## Architectural Constraint

Do not import GitHub transport or authentication concerns into Runtime core.

If a real GitHub implementation requires changes to Protocol execution semantics, stop and return to Design Observation.

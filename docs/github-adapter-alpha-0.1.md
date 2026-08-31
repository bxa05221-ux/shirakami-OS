# Shirakami OS GitHub Adapter α0.1

## Purpose

Define the smallest external GitHub boundary needed to load a Protocol artifact into the existing Shirakami OS Runtime.

## Boundary

```text
GitHub Repository
  ↓
GitHub Adapter
  ↓
Protocol Source
  ↓
Protocol IR
  ↓
Runtime
  ↓
Transition
  ↓
Evidence
```

## Responsibilities

The adapter may:

- locate a repository and protocol artifact;
- retrieve the artifact without changing its semantics;
- preserve repository/path/ref provenance;
- hand the retrieved source to the existing Protocol loading/IR boundary.

The adapter must not:

- interpret domain meaning;
- modify Protocol semantics;
- make Runtime own Landscape semantics;
- promote raw model output to Landscape state;
- introduce authentication, billing, deployment, or provider-specific policy.

## Provenance

Every retrieved Protocol artifact should retain enough provenance to identify:

- repository;
- path;
- ref or revision when available;
- retrieval boundary.

## Non-goals

This α0.1 boundary does not define:

- GitHub authentication policy;
- persistence;
- synchronization;
- conflict resolution;
- remote execution;
- model-provider contracts.

## Verification target

A successful implementation demonstrates only this:

> A Protocol stored outside the Runtime can cross the GitHub Adapter boundary and enter the existing Runtime path without acquiring new domain semantics.

This document is an implementation boundary, not a new Foundation theory.
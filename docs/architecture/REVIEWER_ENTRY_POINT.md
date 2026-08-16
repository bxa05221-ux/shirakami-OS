# Shirakami OS — Reviewer Entry Point

## Purpose

This document is the shortest evidence-backed route for an external reviewer or AI system to inspect the repository without relying on prior knowledge of Shirakami OS.

The review order is intentional: establish the Foundation first, then inspect the Runtime boundary, then inspect implementation and verification evidence.

## Recommended Reading Order

1. **Foundation** — [`spec/README.md`](../../spec/README.md)
2. **Protocol contract** — [`spec/protocol.md`](../../spec/protocol.md)
3. **Adapter contract** — [`spec/adapter-contract.md`](../../spec/adapter-contract.md)
4. **Architecture baseline** — [`docs/Shirakami_OS_Alpha2.2.md`](../Shirakami_OS_Alpha2.2.md)
5. **RFCs** — [`docs/rfc/`](../rfc/)
6. **Runtime implementation** — [`runtime/`](../../runtime/)
7. **Evidence / observation records** — [`docs/observations/`](../observations/)
8. **Examples / Protocol source artifacts** — [`examples/`](../../examples/) and [`protocols/`](../../protocols/)

## Kernel Boundary

The current implementation should be reviewed around these boundaries:

```text
Human Landscape
      ↓
Matome / Protocol Source
      ↓
Protocol IR
      ↓
Runtime
      ↓
Execution Result
      ↓
Evidence
      ↓
Projection
      ↓
Landscape State
      ↓
Replay / Restore
```

The following are Kernel concerns:

- Landscape State
- Protocol / Protocol IR
- Transition execution
- Evidence preservation
- Projection boundary
- Replay / determinism boundary
- Adapter boundary

The following remain outside the Runtime Kernel:

- Domain-specific meaning
- LLM-specific control flow
- UI rendering
- Backend-specific storage semantics
- Research hypotheses not accepted as Foundation contracts

## Architecture Review Questions

An external review should answer these questions from repository evidence rather than from the project name or README alone.

### Protocol / Runtime

- Does the Runtime execute generic Protocol structure without hard-coded domain meaning?
- Does Protocol define allowed transitions rather than merely encode a workflow sequence?
- Where does semantic authority reside when richer semantics are introduced?

### Evidence

- Is Evidence immutable?
- Can an execution result be traced to the Protocol that produced it?
- Is Evidence distinct from an ordinary operational log?

### Projection / Landscape

- Is Evidence separated from its projection into Landscape State?
- Is Landscape State the state/context used by subsequent Protocol evaluation?
- Is Landscape a runtime state model rather than merely an audit-log read model?

### Replay / Migration

- What level of determinism is actually guaranteed?
- Can Landscape State be reconstructed from preserved Evidence?
- Which migration guarantees are implemented, and which remain hypotheses?

### Comparison with Existing Systems

Do not begin by asking whether Shirakami resembles Event Sourcing, Workflow Engines, Policy Engines, or Agent Frameworks.

Instead ask:

> If the system were reduced to ordinary Event Sourcing plus Workflow execution, which current Kernel responsibilities would be lost?

The answer must be derived from the actual Protocol, Evidence, Projection, Landscape, and Replay boundaries in the repository.

## Evidence Policy

External AI observations are **observations**, not authoritative facts.

Repository code, tests, immutable Evidence, and accepted Foundation/RFC documents are the primary evidence sources.

When external reviews disagree:

```text
External Observation
       ↓
Candidate Question
       ↓
Repository / Test Verification
       ↓
Accepted Evidence
```

Do not silently reconcile contradictory external interpretations.

## Current Review Status

- Repository entry point: established
- Foundation navigation: established
- Protocol contract navigation: established
- Runtime implementation navigation: established
- Observation / Evidence navigation: established
- Event Sourcing / Workflow divergence: pending external review
- Landscape layer placement: pending verification
- Rich Protocol Semantics boundary: deferred
- Migration policy: pending explicit contract

## Review Rule

The reviewer should not infer the project's intended meaning from the name `Shirakami OS`.

Read the Foundation, follow the implementation path, inspect the tests and observations, and only then classify the architecture.

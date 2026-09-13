# Shirakami Protocol Classification α0.1

## Purpose

Define the responsibility classes of Shirakami protocols without changing protocol theory.

This document separates protocols that are continuously active in the background from protocols explicitly selected for an operation, and from the runtime mechanisms that execute them.

## Classification

### A. Background Protocols

Background protocols are continuously active as part of the cognitive operating environment. They observe, maintain, or transform the Landscape context without requiring the user to select them for each operation.

Current designated background protocols:

- 暗問層逆算プロトコル
- 3D位相回転アイゼンハワーマトリクス
- 歪天球

Background operation does not mean automatic decision authority. These protocols must not silently select an application protocol or replace human judgment.

For 暗問層逆算プロトコル specifically, continuous operation means retaining and updating unresolved questions between A面 and B面; it does not mean automatically exposing or declaring a hidden truth.

### B. Application Protocols

Application protocols are explicitly selected or presented by the human for a particular operation.

Current example:

- ThreadRPG

ThreadRPG is optional. Its absence must not prevent the Shirakami Runtime from operating.

The Runtime must not infer or autonomously select an application protocol merely from user content.

### C. Runtime / Governance Mechanisms

These are not application protocols. They provide the execution, validation, routing, exchange, and evidence boundaries required to run protocols.

Current mechanisms include:

- OPPAI
- Protocol Registry
- Protocol IR
- Shirakami Runtime
- Adapter boundary
- Evidence
- verification / protected-operation rules

These mechanisms do not assign domain meaning to a protocol and do not constitute automatic protocol selection.

## Responsibility Matrix

| Class | Components | Activation | Primary responsibility | Human selection required | Semantic authority |
|---|---|---|---|---|---|
| Background | 暗問層 / 3D位相回転アイゼンハワーマトリクス / 歪天球 | Continuous | Maintain the cognitive/background context | No per-operation selection | None |
| Application | ThreadRPG and other explicitly presented protocols | Explicit | Perform the selected operation/projection | Yes | Declared by protocol; human remains final authority |
| Runtime/Governance | OPPAI / Registry / IR / Runtime / Adapter / Evidence | Infrastructure-driven | Route, validate, execute, exchange, and record | No | No domain-semantic authority |

## Activation Boundary

The intended Launch Model distinction is:

```text
Background protocols
        │
        └── continuously maintain Landscape/context

Human
  │
  └── explicitly presents/selects an Application Protocol
          │
          ▼
        OPPAI
          │
          ▼
   Protocol Registry
          │
          ▼
      Protocol IR
          │
          ▼
   Shirakami Runtime
          │
          ▼
       Adapter
          │
          ▼
     External AI
```

Background protocols may affect the available Landscape/context presented to the selected protocol, but they do not replace the explicit human selection boundary.

## Non-goals

- No automatic semantic protocol selection.
- No new cognitive theory.
- No assumption that ThreadRPG is mandatory.
- No conversion of background protocols into autonomous authorities.
- No claim that background operation itself proves a protocol's model-specific effect.

## Verification Boundary

This classification is an architectural responsibility boundary. Individual protocols still require their own implementation and activation verification.

A protocol being classified as Background does not by itself establish that its runtime implementation is complete or continuously operational.

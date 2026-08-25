# Shirakami Model v4.1 → Shirakami OS Migration

Status: migration design / implementation boundary test

## Purpose

This document preserves the v4.1 implementation as a prototype and maps its responsibilities onto the current Shirakami OS architecture.

The v4.1 prototype is not treated as a new normative architecture. It is a migration source for existing working behavior.

## Source components

| v4.1 component | Current Shirakami OS boundary | Migration rule |
|---|---|---|
| `CoreMemory` | Landscape / Memory | Keep as Landscape data; do not make Runtime own human semantic truth. |
| `RawLog` | Observation / Evidence input | Preserve raw records; do not equate raw logs with normative Evidence. |
| `CompressedContext` | Context / Matome projection | Treat master + deltas as a context representation, not Runtime-owned meaning. |
| `ShirakamiProcessor` | Runtime orchestration + Model Adapter | Split protocol execution from model/backend invocation. |
| `_call_claude_processor` | External Model Adapter | Backend-specific behavior must leave the Runtime. |
| v4.1 prompt rules | Protocol / Protocol IR | Move domain/protocol semantics out of Runtime code. |
| `_parse_response` | Adapter boundary / validation | Parse and validate model output before any state transition. |
| `append_diff(result)` | Transition → Evidence → Landscape | Never persist an unvalidated model interpretation directly as state. |
| `ShirakamiIntegrator` | Coordination / future protocol-driven integration | Aggregate observations without becoming an autonomous authority. |

## Required boundary

The migration target is:

```text
Landscape
    ↓
Context Snapshot
    ↓
Protocol / Protocol IR
    ↓
Runtime
    ↓
Model Adapter
    ↓
External AI
    ↓
Proposal / Observation
    ↓
Eligibility / Validation
    ↓
Transition
    ↓
Evidence
    ↓
Landscape
```

The Runtime must not contain hard-coded knowledge of:

- 暗問層
- 三極化
- U / I / S
- adopted pole
- domain-specific interpretation

Those belong to the protocol or to an external interpretation/proposal stage.

## First migration slice

The first safe slice is deliberately small:

1. Preserve v4.1 raw input/output behavior as a historical prototype.
2. Represent the v4.1 processing request as Protocol input.
3. Invoke the model through an adapter boundary.
4. Treat model output as an observation/proposal, not as State Truth.
5. Validate the proposal before producing a Transition.
6. Capture the Transition as Evidence.
7. Apply the resulting Evidence to Landscape state.

## Non-goals

This migration does not:

- redefine the 暗問層逆算プロトコル;
- introduce new semantic rules;
- replace the current minimal Runtime vertical slice;
- declare v4.1 a normative specification;
- make Claude a required backend.

## Relationship to the existing executable slice

The current OS already exposes the minimal path:

`Landscape → Protocol → Runtime → Observable Transition → Evidence → Landscape`.

This migration extends that path by inserting the replaceable external-model boundary without changing the Runtime's ownership of domain meaning.

## Verification target

Success means the same v4.1-style processing can be exercised while the Runtime remains unaware of the meaning of the protocol.

Failure conditions include:

- Runtime code branching on v4.1 domain concepts;
- direct promotion of model output to Landscape state;
- backend-specific logic inside Runtime;
- loss of raw input/output lineage.

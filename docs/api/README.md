# Shirakami OS API α0.1

Shirakami OS API α0.1 is the first minimal external interface for the current Runtime boundary.

## Position

```text
External Application
        |
        v
  Shirakami OS API
        |
        v
     Runtime
        |
   +----+----+
   |         |
Protocol   Context
   |
   v
Adapter / Model
   |
   v
Observation / Proposal
        |
        v
    Transition
        |
        v
     Evidence
        |
        v
    Landscape
```

The API does **not** expose a model provider as the architectural boundary. Claude, GPT, Gemini, or another backend remains behind an Adapter.

## Initial endpoints

### `POST /v1/execute`

Apply a Protocol to a supplied Context through the Runtime.

The response may contain an execution result, an observable Transition, and an Evidence reference. A model response is not automatically treated as committed Landscape state.

### `POST /v1/observe`

Record an observation/proposal without committing a Landscape state transition.

This is the explicit boundary between what a model or external observer proposes and what the Runtime accepts as a transition.

### `GET /v1/evidence/{evidence_id}`

Retrieve an immutable Evidence record for an observable transition.

## α0.1 non-goals

- No authentication contract yet.
- No provider-specific endpoint.
- No billing or quota contract.
- No domain-specific Protocol semantics in the Runtime.
- No automatic promotion of model output to Landscape truth.
- No deployment URL is defined yet.

## Relationship to v4.1

The v4.1 prototype is treated as a migration source. Its Memory, Raw Log, compressed Context, Processor, and Integrator responsibilities are being separated across Landscape/Memory, Context, Protocol, Runtime, Adapter, Observation/Proposal, Transition, and Evidence boundaries.

The API therefore exposes the **OS boundary**, not the old v4.1 implementation directly.

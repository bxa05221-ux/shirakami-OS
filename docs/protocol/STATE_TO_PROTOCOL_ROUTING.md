# State-to-Protocol Routing Protocol

## MVP status

Draft v0.1 — executable routing slice.

## Purpose

This protocol connects AIwitness-derived Evidence and Context State to the
3D phase-rotating Eisenhower matrix and uses the resulting state to select
compatible Protocol candidates.

It does not make a final human decision and it does not execute the selected
Protocol.

## MVP flow

```
Evidence
  ↓
AIwitness / Context
  ↓
3D Matrix State
  ↓
Protocol Routing
  ↓
Protocol Candidate
```

The next implementation layer can add Prompt Assembly and Runtime execution.

## State boundary

The MVP uses three explicit matrix dimensions:

```yaml
matrix:
  priority: 2
  phase: 1
  relation: 3
```

The numerical meaning of each dimension remains domain/protocol-defined.
The important requirement at this stage is deterministic state reproduction.

## Protocol registry

A Protocol declares the matrix states it accepts and the Evidence it requires:

```yaml
protocol.alpha:
  accepted_states:
    - priority: 2
      phase: 1
      relation: 3
  required_evidence:
    - E-001
```

If required Evidence is missing, routing returns `blocked` rather than
inventing missing information.

## Human boundary

```
Matrix
  ↓
Routing
  ↓
Protocol candidate
  ↓
[Human / application-specific execution boundary]
```

The routing layer is orchestration, not authority.

## Reconstruction

A routing event must eventually be able to reference:

- Context version
- Evidence references
- Matrix state
- Protocol registry/version
- selected Protocol
- Prompt version
- Runtime version
- Simulation result
- Human decision

This permits the later question:

> Why was this Protocol selected at this time?

to be answered from recorded state rather than reconstructed from AI memory.

## Verification target

The first MVP succeeds if the same explicit Context and Evidence reproduce:

1. the same Matrix State;
2. the same compatible Protocol candidates;
3. the same selected Protocol;
4. a blocked state when required Evidence is absent.

No external AI provider is required for this test.

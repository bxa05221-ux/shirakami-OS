# Shirakami Repository Landscape

## Status

This document records the current repository boundary as an observation, not as a new implementation layer.

## Repository Roles

| Repository | Role | Authority |
|---|---|---|
| `shirakami-model` | Cognitive model, principles, conceptual foundation | Conceptual |
| `shirakami-research` | Observations, experiments, hypotheses, Matome | Exploratory |
| `shirakami-specification` | Stable specifications and protocol contracts | Normative |
| `shirakami-OS` | Runtime, reference implementation, adapters, executable artifacts | Implementational |
| `Shirakami-OS-` | Duplicate/legacy-looking repository; do not extend until its role is explicitly established | Unresolved |

## Intended Flow

```text
Landscape
   ↓
Observation / Research
   ↓
Candidate Protocol / Contract
   ↓
Specification
   ↓
Runtime
   ↓
Adapter / Execution
   ↓
Evidence
   ↓
Observation / Research
```

This is a flow of responsibility, not a requirement that repositories be physically coupled.

## Boundary Rules

1. The Runtime must not become the source of truth for the meaning of a protocol.
2. Research artifacts are not normative merely because they exist in GitHub.
3. A specification becomes normative only after explicit stabilization.
4. GitHub is an adapter/observation environment, not the definition of Shirakami OS.
5. External services such as GitHub, Supabase, and AWS remain replaceable infrastructure unless a specification explicitly says otherwise.
6. Do not add new infrastructure merely to solve a repository-organization problem.

## Current Observation

The `shirakami-OS` repository already contains separate areas for documentation, protocols, runtime, plugins, examples, products, and applications. The runtime also contains GitHub-specific landscape/adapter components. This indicates that GitHub integration is already an implementation concern, while the normative specification boundary is still being separated.

## Next Stabilization Targets

- Keep `shirakami-OS` focused on Runtime and reference implementation.
- Move only **stable, normative** contracts into `shirakami-specification`.
- Keep experiments and observations in `shirakami-research`.
- Keep the cognitive model distinct from the Runtime.
- Treat `Shirakami-OS-` as unresolved until observed and explicitly classified.

## Principle

> GitHub is part of the Landscape we can observe. It is not the Landscape definition itself.

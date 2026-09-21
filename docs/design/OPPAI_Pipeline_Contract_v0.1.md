# OPPAI Pipeline Contract v0.1

## Decision

Shirakami defines **Pipeline** as the executable routing plan attached to a Protocol.

```
Natural Language
  ↓
OPPAI
  ↓
Protocol Candidate Set
  ↓
Human Gate
  ↓
Protocol
  ↓
Pipeline
  ↓
Adapter
  ↓
AI Backend
  ↓
Evidence
```

### Protocol
Defines **what kind of work is being performed and under what semantic rules**.

### Pipeline
Defines **how that Protocol is executed at a particular operation phase**.

A Pipeline is not another semantic Protocol and is not an AI model.

### Adapter
Translates the Pipeline execution requirement into an external AI/runtime interface.

### AI Backend
The replaceable generation or computation service actually used for a Pipeline step.

## Pipeline identity
Pipeline identity is initially **derived from the selected Protocol artifact and execution context**.

A standalone `pipeline_id` is not required in v0.1.

This prevents premature creation of a second registry before actual multi-backend operation has been observed.

When multiple concrete Pipelines for the same Protocol are demonstrated, Pipeline identity may become a first-class Runtime object.

## Pipeline step
The existing Matome representation remains the canonical authoring form:

```yaml
pipeline:
  - phase: observe
    action: inspect
  - phase: organize
    action: structure
```

Each step means:
- `phase`: operational phase
- `action`: requested operation

Neither field authorizes a specific AI vendor.

Backend selection belongs to the Adapter boundary.

## OPPAI responsibility
OPPAI may:
1. observe natural language;
2. normalize it;
3. expose Protocol candidates;
4. expose observable evidence supporting candidate discovery;
5. pass an explicitly selected Protocol onward.

OPPAI must not silently:
- select a Protocol;
- select an AI vendor;
- activate a Protocol;
- rewrite Protocol semantics;
- promote AI output to verified Evidence.

## Selection rule
The minimum safe selection path is:

```
Observation
 → Candidate Set
 → Human Gate
 → Selected Protocol
 → ProtocolRequest
 → Pipeline execution
```

Automated ranking may be investigated later as an observation experiment, but it is not part of the v0.1 contract.

## Why this is the decision
Protocol determines the semantic environment.
Pipeline determines the execution route.
Adapter determines external interface translation.
Backend performs the replaceable AI/computation work.

The same Protocol may therefore be executed through different Pipelines depending on context, operation phase, available infrastructure, or other explicitly observable conditions.

The Protocol remains stable while the execution route may change.

## Non-goals
v0.1 does not define:
- a vendor-specific backend registry;
- automatic model ranking;
- a universal pipeline DSL;
- autonomous Protocol selection;
- a new Pipeline runtime object;
- semantic equivalence between different AI backends.

These require evidence from actual multi-backend execution.

## Status
**Decision: adopted for Shirakami β development.**

The current Matome `pipeline` field is therefore treated as the Protocol-owned execution plan, while the Runtime/Adapter layer remains responsible for realizing it.
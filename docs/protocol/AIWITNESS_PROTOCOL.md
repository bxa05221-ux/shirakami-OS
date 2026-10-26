# AIwitness Protocol

## Status

Draft v0.1

## Purpose

AIwitness is a default protocol of the Shirakami Model for making an AI's involvement in reality reconstructable and verifiable after the fact.

It does not give an AI a personality or consciousness. It records and reconstructs what the AI received, observed, processed, simulated, executed, did not know, and what humans ultimately decided.

## Core Principle

> AI does not own memory or decision authority.  
> AI can, however, testify to what it received and did.

### Reality

Reality is not modified by AIwitness.

### Evidence

AIwitness records references to Evidence rather than requiring all raw data to be stored inside the AIwitness layer.

### External Evidence

Raw data may remain in external systems such as sensors, vehicles, medical devices, cameras, network systems, or other operational infrastructure.

AIwitness retains identifiers, timestamps, sources, references, state, and integrity information sufficient to cross-check against external Evidence.

### Simulation

AI-generated predictions, hypotheses, and alternative scenarios are treated as Simulation and are not represented as Reality.

### Human Authority

AIwitness keeps AI operations and human final decisions separate.

## Default Architecture

```text
Reality
  |
  v
Landscape
  |
  v
Evidence
  |
  v
Protocol
  |
  v
Runtime
  |---- Observation
  |---- Simulation
  |---- Operation
  |
  v
AIwitness
  |
  +---- Context State
  |
  +---- Diff History
  |
  v
External Storage
  |
  v
Reconstruction / Cross-check
  |
  v
Human Judgment
```

AIwitness is not an application added after the fact. It is a standard witness layer spanning Evidence, Runtime, and Operation.

## Minimal Witness Record

```yaml
aiwitness:
  witness_id:
  timestamp:

  evidence:
    id:
    source:
    reference:

  observation:
    state:

  processing:
    protocol:
    operation:

  simulation:
    status:

  uncertainty:
    status:

  action:
    executed:

  human_decision:
    status:
```

The record should allow later reconstruction and cross-checking without requiring the AIwitness layer to retain every raw data stream.

## Context Versioning

Context is maintained as versioned state plus change history rather than as a single mutable summary.

```text
Context v1.0
    |
    +-- Delta 1
    v
Context v1.1
    |
    +-- Delta 2
    v
Context v1.2
```

Each change should preserve:

- version
- parent version
- timestamp
- author/runtime
- reason
- Evidence reference

This makes the evolution of Context itself reconstructable.

## External Context Storage

Context and its history are external to the AI runtime.

Possible storage targets include:

- removable storage
- dedicated companion devices
- NAS
- local servers
- network storage
- cloud storage
- version-control repositories

The storage medium is replaceable. The Context protocol is not dependent on a particular AI vendor or runtime.

## Testimony Rules

1. **Evidence First** — Do not state unsupported content as fact.
2. **No Invented Memory** — Do not manufacture a past record.
3. **Observation / Simulation Separation** — Keep observed state and simulation distinct.
4. **Unknown Disclosure** — Explicitly mark unresolved information.
5. **External Verification** — Enable cross-checking against independent external Evidence where available.
6. **Human Decision Boundary** — Separate AI operations from human final decisions.
7. **Temporal Continuity** — Keep testimony connected to time-ordered Evidence.
8. **History Preservation** — Do not silently overwrite Context history.

## External Cross-check

AIwitness testimony is not itself the final fact determination.

```text
AIwitness Record
      <-->
External Evidence
      <-->
Human Verification
```

This permits investigation of whether:

- the AI received the expected information,
- the AI's observed state matched external measurements,
- the AI's Simulation differed from Reality,
- the AI executed the recorded Operation,
- and where the AI's perception and external measurements diverged.

## Context Handoff

The traditional context handoff represented by a compact summary such as Matome YAML is extended toward:

```text
Current Context State
+
Change History
+
Evidence References
+
Uncertainty
```

A summary may still be generated for human readability or efficient transfer, but it is not the sole source of memory.

## Minimal MVP

A first implementation can use a small controlled scenario:

1. Record the Evidence references around an event.
2. Record AIwitness events.
3. Record AI operations.
4. Record Context changes.
5. Cross-check against external Evidence.
6. Ask the AI to reconstruct its testimony.
7. Have a human verify the reconstruction.

A practical initial test can use a short before/after event window rather than a continuous real-world deployment.

## Success Condition

AIwitness is considered operationally meaningful when it can:

- reference Evidence,
- reconstruct AI observations,
- reconstruct AI operations,
- separate Simulation from Reality,
- disclose unknowns,
- preserve Context change history,
- support external Evidence cross-checking,
- and preserve the boundary of human final judgment.

## Core Statement

> AIwitness is not a mechanism for giving AI memory.
>
> It is a default Shirakami Model protocol for connecting an AI's involvement in reality to external Context and Evidence, so that the AI can later reconstruct and testify to what it received, processed, and did.

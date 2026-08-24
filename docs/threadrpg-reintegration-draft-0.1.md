# ThreadRPG → Shirakami OS 再統合 Draft 0.1

Status: Draft / Design Only

## 0. Purpose

本書は、ThreadRPGをShirakami OSへ再配置するための設計Draftである。

本Draftでは、ThreadRPGを固定人格シミュレーターとしてRuntimeへ組み込まない。
ThreadRPGは、Landscape上で複数の観測主体を展開し、観測・会議・再観測・圧縮を循環させるProtocol群として扱う。

本書は実装仕様ではない。Foundationおよびnormative specificationを変更しない。

## 1. Core Definition

> ThreadRPGは、Shirakami OSの「多視点観測・会議・圧縮プロトコル群」である。
> Threadは人格ではなく、Perspectiveのインスタンスである。
> 人格的な表現はRendererが担当し得るが、Threadの本質ではない。

## 2. Reintegrated Position

```text
                Shirakami OS
                     │
              ┌──────┴──────┐
              │             │
          Landscape       Protocol
              │             │
              ↓             ↓
        Perspective ←→ Thread
              │             │
              └──────┬──────┘
                     ↓
                Observation
                     ↓
                  Evidence
                     ↓
                  Landscape
                     ↓
                  Renderer
```

### 2.1 Landscape

Landscape is the shared observational basis.
Reality is not modified by the observation protocol.
Unresolved states remain unresolved unless a later observable transition changes them.

### 2.2 Protocol

ThreadRPG's core belongs here as a procedural protocol family:

- independent observation
- conference
- re-observation
- Matome compression
- Evidence recording
- Landscape transition

The Protocol declares the procedure. It does not encode a fixed persona.

### 2.3 Perspective

A Thread is an instance of a Perspective.

A Perspective may define or carry:

- viewpoint
- temperature
- interpretation tendency
- Landscape reference scope
- exploration scope

These are observation parameters, not a mandatory personality definition.

### 2.4 Renderer

Renderer determines how an observation or interaction is presented.

Possible representations include:

- conversational style
- AA
- bulletin-board/thread style
- manga
- UI
- audio

A persona-like presentation may be used by a Renderer, but it is not the architectural definition of Thread.

## 3. ThreadRPG Protocol Flow

```text
ThreadRPG Protocol
        ↓
Perspective（複数）
        ↓
Independent Observation
        ↓
Conference
        ↓
Matome API v3.2
        ↓
Evidence
        ↓
Landscape更新
        ↺
```

The intended cycle is:

```text
Observe → Conference → Compress → Return → Observe again
```

The cycle must preserve differences and unresolved questions rather than forcing premature consensus.

## 4. Protocol Candidates

These are candidates for later Protocol artifacts. They are not yet normative specifications.

### Independent Observation

```text
protocol IndependentObservation:
  requires:
    - perspective.scope != null
  apply:
    - observation = observe(landscape, perspective)
  evidence:
    - record("independent_observation", observation)
```

### Conference

```text
protocol Conference:
  requires:
    - threads.count >= 2
  apply:
    - discussion = compare(observations)
  evidence:
    - record("conference", discussion)
```

### Matome

```text
protocol Matome:
  apply:
    - summary = compress(discussion)
  evidence:
    - record("matome", summary)
```

The pseudo-syntax above is explanatory only and must not be treated as Runtime syntax.

## 5. Existing Shirakami OS Boundaries

The reintegration should use existing architectural areas before introducing new top-level layers.

```text
protocols/
products/
evidence/
runtime/
plugins/
```

A possible future arrangement is:

```text
protocols/threadrpg/
    independent_observation.protocol
    conference.protocol
    matome.protocol

products/threadrpg/
    perspective.yaml
    thread.yaml

evidence/threadrpg/
    trail.json
```

A Renderer artifact may be introduced only when an actual rendering requirement exists. No new top-level `perspectives/` or `renderer/` directory is proposed by this Draft.

## 6. Matome API Relationship

The experimental Matome API v3.2 is an external product artifact and is not itself the definition of ThreadRPG.

The intended relationship is:

```text
ThreadRPG Protocol
        ↓
Perspective
        ↓
Observation / Conference
        ↓
Matome API v3.2
        ↓
Evidence
        ↓
Landscape
```

The API remains experimental. Its contract must not silently become a normative Foundation specification.

## 7. Evidence Role

ThreadRPG Evidence is not an existence proof for the OS.

Its purpose is to carry an observable transition into the next observation.

```text
Observable Transition
        ↓
Evidence
        ↓
Landscape State
        ↓
Next Observation
```

Evidence should preserve unresolved items and the context needed for subsequent observation.

## 8. Non-Goals

This Draft does not:

- add a fixed persona system to Shirakami OS
- move ThreadRPG into the Runtime kernel
- define a normative ThreadRPG API
- create a new top-level architectural layer
- freeze Perspective as a final schema
- convert the experimental Matome API into a stable specification

## 9. Next Observation

The next design questions are intentionally left open:

1. Which ThreadRPG procedures should become concrete Protocol artifacts?
2. What is the minimum Perspective representation required by independent observation?
3. Which Matome API operations are actually required by ThreadRPG?
4. What Evidence fields are necessary for a subsequent observation?
5. Which parts, if any, require a Renderer artifact?

## 10. Status

Draft 0.1 is a design boundary document only.

It records the current reintegration hypothesis without changing the Foundation Freeze or claiming that the proposed structure is already implemented.

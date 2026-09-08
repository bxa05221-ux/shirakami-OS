# R0010 — 暗問層逆算プロトコル Boundary Experiment

## Purpose

暗問層逆算プロトコルを、既存の Protocol Loader → ProtocolIR → Runtime → Evidence → Landscape 経路へ投入し、意味論を Kernel へ移さずにどこまで保持・観測できるかを確認する。

本実験は理論の採用・変更を行うものではなく、既存 Runtime 境界に対する観測である。

## Input fixture

```yaml
input:
  surface:
    utterance: "別に心配してねえよw"
    context: "相手が弱音を吐いた直後"
    timing: "immediate"
  observation:
    joke: true
    silence: false
    aa: false
```

## Protocol path

```text
Matome YAML
  ↓
ProtocolIR
  ↓
Runtime
  ↓
Transition
  ↓
Evidence
  ↓
Landscape Projection
```

## Expected boundary behavior

### Protocol side

The Protocol declares the following domain-specific structure:

- surface_capture
- layer_stripping
- b_side_extraction
- resonance_lock
- reverse_engineering
- consistency_check
- defensive-layer questions
- motivational hypotheses
- reconstruction criteria

These remain Protocol-specific semantics.

### Runtime side

Runtime must not determine:

- what the person's "true" motivation is
- whether a B-side hypothesis is fact
- whether shame, fear, or loss is objectively present
- the meaning of a joke, silence, or AA

Runtime only transports and records the declared execution transition.

## Observation target

The primary observation is whether the question can remain a question rather than being promoted to a Runtime fact.

Specifically, this experiment checks whether the current Evidence/Projection path can preserve enough transition data to distinguish:

```text
observation
  ≠
interpretation
  ≠
truth claim
```

without introducing a new Kernel concept for anmon_layer, A-side, B-side, or "truth".

## Current hypothesis

The existing generic Transition/Evidence boundary is sufficient for the first experiment because the protocol-specific structure can travel as transition data. A dedicated Evidence schema extension is not justified before an observed failure.

## Pass criteria

1. The Matome YAML loads into the existing β0.1 ProtocolIR subset.
2. The protocol reaches the generic Runtime transition boundary.
3. Evidence records the resulting transition without rewriting its semantics.
4. Landscape Projection can expose the resulting state/transition.
5. No Runtime code is required to understand "B面", "暗問層", or "真実".

## Non-goals

- Implementing an anmon-layer interpreter in Kernel.
- Declaring B-side hypotheses as facts.
- Changing the Evidence schema.
- Changing the normative Protocol Specification.
- Establishing a universal theory of human cognition.

## Result status

Experiment artifact prepared. Runtime/CI execution result must be recorded separately from this protocol-side observation; no execution success is claimed merely by the presence of this document.

## Next observation

After CI execution, compare the actual Evidence payload with the expected distinction between observation, interpretation, and truth claim. If the current structure is insufficient, report the concrete loss of information to the research side rather than extending Kernel semantics by assumption.

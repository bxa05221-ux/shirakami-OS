# Shirakami OS — Cognitive Observation Bridge

## Purpose

This document records the current implementation boundary between Shirakami's cognitive-observation research and the Runtime.

It is an implementation bridge, not a new Foundation theory.

## Position

```text
Research / Cognitive Model
        ↓
Cognitive Observation
        ↓
Observable Transition
        ↓
Evidence
        ↓
Protocol / Protocol IR
        ↓
Runtime
        ↓
Landscape Projection
        ↓
Re-observation
```

The bridge exists so that research concepts can be tested against executable Runtime boundaries without silently becoming normative contracts.

## Research Lineage

The current research lineage includes:

```text
AA Thread Simulator Lite
        ↓
Thread RPG
        ↓
Cognitive Observation
        ↓
Shirakami Cognitive Observation Architecture
```

The AA Thread Simulator Lite is treated as an early interaction prototype exploring temperature, ambiguity retention, cooling, and conversation continuity. Thread RPG extends this into multi-perspective thread interaction. The lineage is historical/experimental evidence, not by itself a Foundation contract.

## Cognitive Observation Architecture

The following concepts are research-side observation mechanisms and must not be interpreted as settled Runtime semantics unless explicitly promoted through the specification process.

### Celestial Model

Role: cognitive-space representation.

Question:

> What part of the cognitive space is currently visible, and what remains outside the current view?

### 3D Phase-Rotating Eisenhower Matrix

Role: cognitive-position / phase-rotation model.

Question:

> From which cognitive position is the current Landscape being considered, and how does changing position change what can be observed?

### Cognitive Echolocation

Role: observation mechanism.

Observes:

- cognitive position;
- Landscape change;
- newly observable relations;
- unresolved gaps;
- hidden questions.

### Anmon Layer

Role: unresolved-question layer.

Rule:

> Do not force an unresolved question into a premature answer. Preserve it for subsequent observation.

### AASS

Role: operational connection under research.

The formal definition of AASS must be taken from the existing research/protocol source. This document intentionally does not redefine the acronym or extend its theory.

## Runtime Boundary

The Runtime must receive observable state/evidence through explicit contracts.

It must not infer that a research-side observation is authoritative merely because it exists.

```text
Observation
    ↓
Evidence
    ↓
Contract validation
    ↓
Protocol IR
    ↓
Runtime transition
```

Interpretation remains distinct from Observation.

```text
Observation ≠ Interpretation
Interpretation ≠ Truth
Evidence ≠ Meaning by itself
```

## Landscape Observer

`apps/landscape-observer/` is the first candidate application for exercising this bridge.

Its intended loop is:

```text
User interaction
      ↓
Observation
      ↓
Evidence
      ↓
Landscape projection
      ↓
Re-observation
      ↓
New Evidence
```

The first executable milestone remains deliberately small: demonstrate two distinct Evidence objects and preserve their relationship without mutating the first Evidence.

## Research-to-Runtime Rule

1. Research concepts may be observed and implemented experimentally.
2. Experimental implementation does not automatically make a concept normative.
3. Stable contracts must be promoted through the specification repository.
4. Runtime code must not acquire domain-specific cognitive meaning merely to make an experiment pass.
5. If the Runtime boundary cannot express a research observation cleanly, record the limitation rather than silently changing the theory.

## Why This Bridge Exists

A memory system can collect and retrieve fragments without representing the changing relationship between a person and those fragments.

The Shirakami research direction instead asks whether Landscape change can be made observable while preserving uncertainty, evidence identity, and human agency.

The implementation question is therefore:

> Can cognitive observation be represented as explicit, traceable transitions without turning the Runtime into an interpreter of human psychology?

That question is open to verification.

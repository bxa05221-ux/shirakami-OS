# AIwitness Runtime Integration

## MVP status

Draft v0.1 — Prompt/Simulation witness integration.

## Purpose

This layer closes the first executable trace:

```
Evidence
  ↓
Context
  ↓
Matrix
  ↓
Protocol
  ↓
Prompt
  ↓
Simulation
  ↓
AIwitness
```

The witness record links the Simulation back to the Evidence references,
Context version, Prompt and Protocol that produced it.

## Boundary

AIwitness records what the Runtime processed and simulated. It does not turn
Simulation output into Reality and does not make a human decision.

## Reconstruction key

A witness can identify:

- Evidence references
- Context version
- Prompt ID
- Protocol ID
- Simulation ID
- Simulation status
- uncertainty

The remaining Human Decision / Operation boundary is intentionally outside
this MVP slice.

## Verification target

The same Prompt and Simulation must produce a witness whose references are
internally consistent. Mismatched Prompt/Simulation identifiers are rejected.

# R0010-B: Question Preservation Boundary Test

## Purpose

Test whether the current Runtime/Evidence path can preserve the distinction between observation, question, and provisional hypothesis without promoting interpretation to truth.

## Input fixture

```yaml
observation:
  surface:
    utterance: "別に心配してねえよw"
    context: "相手が弱音を吐いた直後"
    timing: "immediate"

question:
  text: "なぜ、このタイミングで冗談を言ったのか？"
  status: open

hypothesis:
  text: "相手を心配している可能性"
  status: provisional
```

## Boundary expectation

The Runtime must not decide that the hypothesis is true.

The experiment is successful if the observation, open question, and provisional hypothesis can pass through the existing Protocol IR → Runtime → Transition → Evidence boundary without being rewritten into a single semantic truth claim.

## Non-goals

- No new Evidence schema is introduced by this experiment.
- No Kernel-specific concepts for A-side, B-side, Anmon Layer, or truth are introduced.
- No psychological diagnosis or causal claim is made.

## Pass criteria

1. The fixture can be represented as Protocol-owned data.
2. The existing Runtime path can carry the data without semantic interpretation.
3. Evidence preserves the distinction between observation, question, and provisional hypothesis at the recorded transition boundary.
4. Landscape Projection does not promote the hypothesis to established fact.

## Failure condition

If the current Evidence representation necessarily collapses observation, question, and provisional hypothesis into an undifferentiated or authoritative semantic claim, record that as an implementation/specification gap and return it to research. Do not solve the gap by silently changing the Kernel.

## Status

Experiment fixture prepared. Execution success is not claimed by this document alone.

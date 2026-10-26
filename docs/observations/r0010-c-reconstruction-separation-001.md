# R0010-C — Reconstruction Separation Boundary

## Purpose

Test whether the current Runtime/Evidence path can carry an original surface observation and a reconstructed surface as distinct Protocol-owned data, without collapsing the reconstruction into the original observation or treating a hypothesis as fact.

## Input fixture

```yaml
observation:
  original_surface:
    utterance: "別に心配してねえよw"
    context: "相手が弱音を吐いた直後"
    timing: "immediate"

  question:
    text: "なぜ、このタイミングで冗談を言ったのか？"
    status: open

  hypothesis:
    text: "相手を心配している可能性"
    status: provisional

  reconstruction:
    reconstructed_surface:
      utterance: "……まあ、無理すんなよw"
      status: reconstructed
    source:
      from: hypothesis
      preserves: original_temperature
```

## Expected boundary

1. The fixture remains representable as Protocol-owned data.
2. The existing Loader/IR/Runtime path carries the fixture without requiring Kernel knowledge of `original_surface`, `question`, `hypothesis`, or `reconstructed_surface` semantics.
3. Evidence preserves the distinction between the original observation and the reconstructed surface.
4. Landscape Projection does not overwrite the original observation with the reconstruction.
5. The provisional hypothesis remains provisional; reconstruction is not emitted as factual history.

## Non-goals

- No new Runtime state is introduced.
- No new Evidence schema is introduced.
- Runtime does not decide whether the hypothesis is psychologically true.
- Runtime does not merge A面/B面 or determine a person's "true" state.

## Interpretation

A pass demonstrates a structural boundary only: the Runtime can transport multiple semantically distinct Protocol-owned artifacts without interpreting their domain meaning. A failure is an implementation/specification gap to be returned to research; it must not be resolved by silently adding Anmon Layer semantics to the Kernel.

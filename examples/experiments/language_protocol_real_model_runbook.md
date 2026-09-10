# Language Protocol Real-Model Runbook

Status: operator-run experiment

## Purpose

Run the same Landscape/task input through the four directly adopted language protocols using the existing external Adapter boundary.

Protocols:

- `shirakami-3d-pruim`
- `shirakami-anmon-layer-reverse`
- `shirakami-cognitive-echolocalization-hypothesis-v0.1`
- `shirakami-thread-rpg-v3.2`

## Boundary

The Runtime is unchanged. The experiment does not inject protocol semantics into Runtime Core and does not define AI personality.

The external model provider is executed only in an operator environment with its own credentials. Credentials must not be committed to the repository.

## Execution

From the repository root, provide the same Landscape/task text on stdin to the comparison harness:

```bash
printf '%s\n' 'YOUR LANDSCAPE OR TASK TEXT' | python examples/experiments/compare_language_protocols_same_landscape.py
```

The current comparison harness uses a deterministic adapter for boundary verification. For an actual model observation, run the provider-specific experiment harness in an environment where the provider credential is configured.

## Observation record

Preserve:

- raw input
- protocol ID
- canonical input
- model output
- OPPAI observation
- Evidence
- execution environment/model identifier when available
- operator corrections, if any
- unresolved elements

## Interpretation boundary

Do not infer from one run that:

- a protocol is scientifically valid
- a protocol improves model quality
- one model has a superior personality
- cognitive echolocation has been proven
- the model has acquired human-like experience

The experiment records observable differences. Human/research judgment remains outside the Runtime.

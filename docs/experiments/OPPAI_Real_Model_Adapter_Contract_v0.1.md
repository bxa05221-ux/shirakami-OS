# OPPAI Real Model Adapter Contract v0.1

Status: integration contract

## Objective

Connect a real downstream AI model without changing the OPPAI boundary.

## Adapter contract

A model adapter receives:

```text
canonical_prompt
context
```

and returns an opaque `adapter_output`.

The adapter MUST NOT rewrite OPPAI observations. The adapter MUST NOT be treated as the source of truth for raw user input, corrections, unresolved items, or Evidence.

## Required separation

```text
OPPAI observation ───────────────┐
                                 ├─ Runtime result
Model adapter output ────────────┘
```

The two streams remain distinguishable after execution.

## First real-model test

Use one inexpensive model adapter first. Compare the same task with:

1. direct model interaction
2. OPPAI + the same model

Keep model, task, and context as constant as practical.

Record:

- raw user input
- OPPAI observation
- canonical prompt candidate
- model output
- human correction/recovery turns
- subjective operational notes

## Success criterion

The first test is successful if the complete path executes without requiring the user to manually formulate an OPPAI-specific prompt and the observations remain inspectable.

Quality or cost superiority is a separate hypothesis and must not be inferred from successful execution alone.

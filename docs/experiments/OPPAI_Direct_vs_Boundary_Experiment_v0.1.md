# OPPAI Direct vs Boundary Experiment v0.1

Status: experiment specification

## Question

Does an OPPAI boundary reduce human repair work and operational friction when the same downstream model is used?

## Control

Human input is sent directly to the model using the ordinary chat interface.

## Experimental condition

The same human input passes through OPPAI before reaching the same model.

```text
CONTROL
Human → Model

OPPAI
Human → OPPAI → Protocol → Runtime → Model
```

## Keep constant

- model
- task
- available context
- task order
- evaluation criteria

## Record

For each turn record:

1. elapsed human interaction time
2. number of user corrections
3. number of re-explanations
4. context-recovery requests
5. task completion outcome
6. whether the user voluntarily continues the interaction
7. qualitative comfort/friction note

## Primary observation

The primary question is not raw model benchmark performance. It is whether the human can operate the system without adapting their ordinary thought process to machine-specific prompt conventions.

## Interpretation boundary

A positive result supports the usefulness of the boundary for the tested task and model. It does not establish universal model parity or superiority.

## Next implementation step

Connect one real model adapter and execute paired tasks under this protocol. Preserve raw inputs and OPPAI observations as Evidence so that downstream interpretation remains reviewable.

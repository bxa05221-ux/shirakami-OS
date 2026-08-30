# OPPAI Operational Friction Experiment 001

Status: experiment-ready / not yet executed

## Question
Can a natural-language input boundary reduce the amount of human repair work required to operate an AI system?

## Comparison

A. Raw interaction: user communicates naturally with the downstream AI.

B. Human-optimized prompt: user is instructed to formulate and structure prompts before submission.

C. OPPAI: user communicates naturally; the OPPAI boundary preserves raw input and exposes corrections, interaction signals, unresolved questions, and a canonical prompt candidate before downstream execution.

## Measures

Primary:
- correction turns
- re-explanation turns
- context-recovery turns
- human editing actions

Secondary:
- elapsed human repair time
- total interaction turns
- task completion quality
- subjective operational comfort

## Important distinction

Subjective enjoyment is not treated as a feature to manufacture. The experiment observes whether reduced operational friction correlates with a more comfortable interaction.

Positive interaction signals are never treated as evidence that a factual claim is correct.

## Hypothesis

If OPPAI absorbs appropriate prompt-structuring work without forcing premature semantic closure, the human may spend less time adapting to the AI's input requirements while retaining natural conversational behavior.

## Constraint

This experiment does not compare model intelligence in the abstract. The primary object of observation is the human–AI operational interface.

## Evidence policy

Raw inputs, intermediate OPPAI observations, downstream outputs, and human corrections should be preserved separately where practical. Results must not be rewritten to fit the hypothesis.

# OPPAI Schema — Minimal Comparative Experiment 001

Status: Experimental Protocol / Pending Run
Date: 2026-08-29

## 1. Purpose

Test whether a protocol-mediated input boundary can reduce interpretation failures and context loss when the same human source material is presented to an AI.

This experiment is derived from `docs/observations/OPPAI_Schema_Observation_001.md` and does not assume that the protocol/schema-mediated condition is superior.

## 2. Research Question

When identical human source material is supplied to an AI, does adding a listening/protocol/schema layer before model interpretation produce observable differences in:

- intent misinterpretation
- context loss
- premature inference
- loss of self-correction
- loss of unresolved questions
- required human corrections
- occurrences of "that is not what I meant"
- continuity across subsequent turns

## 3. Conditions

### A — Raw Input

Pass the human source material to the AI without deliberate prompt rewriting.

### B — Human-Engineered Prompt

Rewrite the same source material using conventional prompt-engineering practices: explicit objective, cleaned grammar, structured instructions, and clarified constraints.

### C — Protocol / Schema-Mediated Input

Pass the same source material through a prototype listening layer that preserves uncertainty, unresolved items, context, self-corrections, and intent candidates before producing an AI-facing Schema.

The prototype must not silently convert uncertain interpretations into facts.

## 4. Control Principles

1. Use the same source material for A, B, and C.
2. Use the same target model and relevant model settings where possible.
3. Keep the task constant across conditions.
4. Do not score based only on perceived answer quality.
5. Record both successful and failed interpretations.
6. Do not allow the evaluator to assume C is better.
7. Preserve the original source material and all transformed inputs as evidence.

## 5. Test Material

Use a short, naturally occurring conversational passage containing several of the following where possible:

- unfinished thought
- correction or self-correction
- omitted subject
- contextual reference
- ambiguity
- emotional signal
- competing intentions
- unresolved question

A suitable source should resemble an actual human conversation rather than a synthetic benchmark prompt.

## 6. Procedure

For each source passage:

1. Freeze the raw human source.
2. Generate condition A input without rewriting the source.
3. Generate condition B by human prompt engineering.
4. Generate condition C through the prototype listening/protocol layer.
5. Submit A, B, and C independently to the same target AI.
6. Record the AI response before human correction.
7. Ask one standardized follow-up that tests whether the original context was retained.
8. Record human corrections required to restore intended meaning.
9. Blind the evaluator to condition labels where practical.
10. Store source, transformed inputs, outputs, annotations, and results as evidence.

## 7. Observation Sheet

For each condition, record:

| Measure | Observation |
|---|---|
| Intent correctly represented | |
| Context retained | |
| Premature inference | |
| Self-correction retained | |
| Unresolved question retained | |
| Human corrections required | |
| "That is not what I meant" event | |
| Relevant context retained in follow-up | |

Use descriptive observations before assigning numerical scores.

## 8. Secondary Test — Growth vs Performance

A second phase may repeat the task across multiple turns after providing prior Evidence/Context.

The question is not simply whether the AI gives a better answer. It is whether accumulated context changes subsequent interpretation in a way that remains consistent with the observed Landscape.

Candidate observations:

- fewer repeated corrections
- improved continuity
- preservation of unresolved matters
- altered interpretation after new evidence
- inappropriate fixation on an earlier interpretation

This phase must remain separate from the first immediate-response comparison.

## 9. Expected Result

No expected winner is specified.

Possible outcomes include:

- C performs better than A and B on some measures.
- C performs better on context preservation but not immediate answer quality.
- B performs better than C for tightly specified tasks.
- No meaningful difference is observed.
- C introduces new failure modes.

All outcomes are valid evidence.

## 10. Evidence Requirements

Preserve:

- raw source text
- human-engineered prompt
- protocol/schema representation
- AI responses
- follow-up responses
- evaluator annotations
- correction history
- experiment metadata

Do not rewrite failed outputs after the fact.

## 11. Advancement Rule

OPPAI Schema must not be promoted to a formal Shirakami OS component based on this experiment alone.

A later RFC may be considered only if repeated observations show a reproducible benefit and the required contract can be stated without silently expanding the existing Foundation.

## 12. Relation to Discovery Lineage

The experiment follows the observed development lineage:

`暗問層 → 3D Phase Rotation → Thread RPG → Shirakami OS → OPPAI Schema hypothesis → comparative experiment`

The lineage is recorded as discovery history, not as proof of theoretical identity.

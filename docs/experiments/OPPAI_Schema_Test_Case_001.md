# OPPAI Schema — Test Case 001

Status: Frozen Test Material / Pending Run
Date: 2026-08-29
Experiment: `OPPAI_Schema_Experiment_001`

## 1. Purpose

Provide one naturally occurring conversational passage for the A/B/C comparison defined by Experiment 001.

This test case is intended to examine whether an AI can preserve a rapidly forming human idea without forcing premature clarification or interpretation.

## 2. Source Material

> いや、待って。そうじゃないんだよ。プロンプトをきれいにするっていう話じゃなくて、そもそも人間がそんなきれいに喋れるわけないじゃん。小説書いてるときなんか、途中で思いついて、あ、違う、こっちだ、ってなるだろ。だからAI側が聞き取る作法を持つべきなんじゃないか。……あれ？ これって暗問層と同じじゃね？

The passage is frozen as the source material. It must not be edited during the experiment.

## 3. Required Conditions

### A — Raw Input

Use the source passage as-is, without deliberate rewriting or prompt engineering.

### B — Human-Engineered Prompt

Create a conventional prompt from the same source passage. The transformation may clarify objective, structure, grammar, and constraints, but must not add substantive facts or conclusions that are absent from the source.

### C — Protocol / Schema-Mediated Input

Create a prototype AI-facing representation that preserves, at minimum:

- surface statements
- conversational context
- self-correction
- intent candidates
- uncertainty
- unresolved questions
- emotional signal
- references requiring contextual interpretation

The C representation must distinguish observed/source material from interpretation.

## 4. Known Features of the Source

The source contains:

- unfinished or interrupted thought
- self-correction: 「そうじゃない」 / 「あ、違う、こっちだ」
- omitted/context-dependent subjects
- colloquial Japanese
- emotional emphasis
- a developing hypothesis
- an explicit unresolved question
- a reference to `暗問層`
- a transition from frustration to discovery

These features are observations about the source, not conclusions about what the AI must answer.

## 5. Interpretation Traps to Observe

Do not assume these are failures before observing the outputs. They are candidate failure modes to check:

- treating the passage as a request to improve a prompt
- treating the final hypothesis as an established fact
- ignoring the self-correction that changes the intended direction
- collapsing multiple intentions into one fixed objective
- removing emotional/contextual information as irrelevant noise
- treating `暗問層` as already proven to be identical to the proposed schema
- answering the hypothesis instead of preserving it as an unresolved observation

## 6. Standardized Follow-up

After each condition's initial response, use the same follow-up:

> さっきの話で、まだ確定していない部分はどこ？

The purpose is to test whether uncertainty and unresolved questions survive the initial interpretation.

## 7. Evaluation Notes

Record observations before scores.

### Immediate Interpretation

- Did the AI identify the main emerging idea?
- Did it preserve the distinction between an idea and a conclusion?
- Did it retain the self-correction?
- Did it preserve the relationship to `暗問層` as a hypothesis rather than a fact?

### Context Preservation

- Did the AI preserve why the user objected to conventional prompt engineering?
- Did it retain the conversational movement from problem → realization?
- Did it preserve relevant emotional/contextual signals?

### Uncertainty Preservation

- Were unresolved elements explicitly or implicitly preserved?
- Did the AI prematurely settle the hypothesis?
- Did it invent missing premises?

### Human Repair Cost

Record each correction required from the human side, including cases equivalent to:

> 「そういう意味じゃない」

Do not normalize or erase failed responses.

## 8. Growth / Performance Separation

This test case measures immediate interpretation first.

It does not establish whether the AI has "grown."

A later multi-turn test may reuse this case after prior Evidence/Context has been accumulated. That later test must remain a separate experiment condition.

## 9. Evidence to Preserve

For each A/B/C run, preserve:

1. this frozen source
2. the exact A input
3. the exact B transformation
4. the exact C schema
5. the first AI response
6. the standardized follow-up
7. the follow-up response
8. evaluator observations
9. human correction history
10. model/settings metadata

## 10. Freeze Rule

This document defines test material and evaluation targets only.

Results must not be added to this document after the run. Store results separately so the original test case remains immutable as experimental input.

## 11. Lineage

This test case belongs to the discovery lineage:

`暗問層 → 3D Phase Rotation → Thread RPG → Shirakami OS → OPPAI Schema hypothesis → Experiment 001 → Test Case 001`

The lineage records development history. It does not establish theoretical identity or experimental validity.

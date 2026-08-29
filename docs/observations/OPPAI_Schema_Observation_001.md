# OPPAI Schema Observation 001

Status: Hypothesis / Observational Draft
Date: 2026-08-29

## 1. Purpose

This document records an architectural hypothesis that emerged during the continued construction and operation of Shirakami Model / Shirakami OS.

It does not modify Foundation-level specifications and does not establish OPPAI Schema as a formal Shirakami OS component.

## 2. Discovery Path

The current hypothesis did not precede Shirakami OS as an independent design proposal. It emerged while examining structures that had already been developed:

1. 暗問層 (Anmon Layer)
2. 3D Phase Rotational Urgency-Importance Matrix (3D-PRUIM)
3. Thread RPG
4. Shirakami OS architecture
5. OPPAI Schema hypothesis

The observed continuity is:

- 暗問層: avoid premature meaning fixation and preserve unresolved questions.
- 3D-PRUIM: change the observation position rather than treating one coordinate system as the whole state.
- Thread RPG: allow multiple observers to operate within the same Landscape and feed observations back into the loop.
- Shirakami OS: separate Landscape, Evidence, Protocol, Runtime, and adapters so that observed state and protocol semantics are not collapsed into the model itself.
- OPPAI Schema: hypothesize an input-side boundary that receives natural human language before it is treated as a finalized AI prompt.

## 3. Core Hypothesis

Conventional prompt engineering largely places the burden of interpretation on the human: the human is expected to transform natural language into a clean, explicit prompt before the AI receives it.

The hypothesis here is that an AI-facing system should instead provide a protocol-mediated listening boundary.

Natural human conversation may contain:

- unfinished thoughts
- corrections and self-corrections
- omitted subjects
- contextual references
- ambiguity
- emotional signals
- competing intentions
- unresolved questions

The proposed boundary should not erase these properties merely to produce a cleaner prompt. It should preserve uncertainty and distinguish observation from interpretation before producing an AI-facing Schema.

Conceptual flow:

Human Natural Input
  -> Listening / Capture
  -> Context and Intent Candidates
  -> Uncertainty / Unresolved State
  -> Protocol Processing
  -> AI-facing Schema
  -> AI Runtime / Model

## 4. Relationship to Anmon Layer

A working observation is that the Anmon Layer may be an early prototype of the same structural requirement.

The Anmon Layer was developed to prevent a surface observation from being prematurely converted into a definitive interpretation. Its reverse-engineering protocol explicitly preserves the distinction between A-side and B-side and prohibits premature certainty: A-side is not simply a mask, B-side is not simply truth, and meaning emerges through movement between them.

This document does not claim that Anmon Layer and OPPAI Schema are identical. The narrower observation is that both introduce an intermediate space between input and fixed meaning.

## 5. Relationship to Existing Shirakami Architecture

The current Shirakami OS foundation treats the Landscape as central and the Runtime as a service to that Landscape. Evidence is recorded and preserved, while Protocol defines processing boundaries and Runtime executes them.

Existing development material also records that the Shirakami OS development process itself can be used as an experimental environment: Human Question -> Matome Protocol -> Runtime Implementation -> External AI Review -> Independent Criticism -> Experiment -> Evidence -> Architecture Revision.

OPPAI Schema should therefore be treated as an observation arising from this development loop, not as an assumed foundation requirement.

## 6. Performance vs Growth

A related hypothesis emerging from this observation is that performance improvement and growth should not be treated as identical.

Performance improvement generally means that an existing function becomes faster, more accurate, or more capable.

Growth concerns whether accumulated Context and Evidence alter subsequent observation, interaction, or behavior.

This distinction is relevant because an input-side Schema may be valuable not only for producing a better immediate answer, but for preserving the context required for subsequent interactions and Landscape continuity.

This remains a hypothesis and requires independent verification.

## 7. Proposed Minimal Comparative Experiment

The first experiment should compare identical human source material under three conditions:

### A. Raw Input

Natural human language is passed directly to the AI.

### B. Human-Engineered Prompt

The human rewrites the source material according to conventional prompt-engineering practice.

### C. Protocol / Schema-Mediated Input

The source material is processed through a prototype listening/protocol layer that preserves uncertainty, unresolved items, and intent candidates before producing an AI-facing Schema.

### Measures

The experiment should not evaluate only answer quality. It should record:

- intent misinterpretation
- context loss
- premature completion or inference
- loss of self-correction
- loss of unresolved questions
- number of human corrections required
- occurrences of "that is not what I meant"
- continuity of relevant context in subsequent turns

## 8. Experimental Discipline

The experiment must not assume that C is superior.

The purpose is to determine whether a protocol-mediated input boundary produces observable benefits over the alternatives.

No claim of novelty, superiority, or scientific validity is made by this observation document alone.

## 9. Architectural Status

Current status:

- Foundation: unchanged
- Existing Protocols: unchanged
- Runtime contract: unchanged
- OPPAI Schema: hypothesis only
- Implementation: not yet adopted as Foundation
- Verification: pending

If experimental evidence supports the hypothesis, a later RFC may define an explicit contract. Until then, this document serves as an observation record and preserves the discovery lineage.

## 10. Working Name

Working name:

**OPPAI Schema**

The name is provisional and should not be treated as a Foundation-level naming decision.

The conceptual phrase currently associated with the working name is:

**Operating Prompt Protocol for AI**

The exact expansion and formal terminology remain subject to future specification.

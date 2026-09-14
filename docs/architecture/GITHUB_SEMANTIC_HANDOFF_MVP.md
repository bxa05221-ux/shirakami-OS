# GitHub Semantic Handoff MVP

**Version:** 0.1  
**Status:** Experimental  
**Category:** Semantic Handoff

## Purpose

GitHub Semantic Handoff defines a small boundary between a GitHub repository and an AI runtime.

The user does not need to transfer an entire repository to an AI. Instead, a human question is used to select only the repository resources required to investigate that question.

```text
Human Question
      ↓
Semantic Selection
      ↓
GitHub Retrieval
      ↓
Evidence
      ↓
Matome YAML
      ↓
AI Runtime
      ↓
Human Review
```

## Design Principle

> **Do not give the AI the repository. Give the AI the repository evidence required for the question.**

A repository is treated as a source of evidence, not as an authority over the interpretation produced by an AI runtime.

## MVP Boundary

The first implementation deliberately does not attempt to build a general-purpose GitHub agent.

It defines only these responsibilities:

1. Receive a question and repository reference.
2. Determine a minimal semantic selection.
3. Retrieve selected resources.
4. Preserve repository path, ref, and commit identity.
5. Represent the selected evidence as a Matome YAML handoff.
6. Mark insufficiency or conflict through the Anmon boundary.
7. Hand the resulting context to an AI runtime for interpretation.

The AI runtime does not receive implicit permission to expand the retrieval scope.

## Example: Shirakami Self-Review

Question:

> Can Shirakami OS be represented as a model-independent reference architecture?

Initial selection:

```text
README.md
docs/architecture/REVIEWER_ENTRY_POINT.md
docs/architecture/*
spec/*
```

Initial exclusions:

```text
runtime/*
plugins/*
experimental/*
```

The exclusions are not claims that those resources are unimportant. They express that the first question concerns architecture and normative boundaries rather than implementation details.

If the selected evidence is insufficient, the protocol enters the Anmon boundary and produces a candidate request for additional evidence. Retrieval scope is expanded explicitly rather than silently.

## Evidence Rules

Each selected resource should retain:

- repository
- path
- ref
- commit SHA where available
- retrieval purpose
- retrieved content

Interpretation must remain distinguishable from source evidence.

The handoff may distinguish:

- `fact`
- `interpretation`
- `hypothesis`
- `unresolved`
- `protocol`

## Relationship to Shirakami

GitHub Semantic Handoff is an application of the Shirakami boundary model:

```text
Landscape
   ↓
Evidence
   ↓
Protocol
   ↓
Runtime
   ↓
Adapter
   ↓
External AI
```

The GitHub repository occupies the source/evidence side of the boundary. The Semantic Handoff layer determines what portion of that source is relevant to the current question.

This makes the repository itself an experimental Landscape for Shirakami's own architecture.

## What This MVP Is Testing

The MVP tests one concrete proposition:

> **Semantic selection can reduce repository-to-AI context transfer without losing the evidence necessary to answer a defined question.**

A successful experiment should make the selection observable and reproducible, and should make it possible to explain why each selected resource entered the handoff.

## Non-Goals

This MVP does not claim:

- autonomous repository ownership
- autonomous code modification
- complete repository understanding
- universal optimal file selection
- vendor-specific AI integration
- a standardized GitHub protocol

It is an experimental protocol and reference implementation candidate.

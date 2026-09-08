# Shirakami Development Loop

**Codename:** SDL  
**Version:** 0.1  
**Status:** Experimental

## Purpose

Shirakami Development Loop (SDL) is a development method for circulating human discoveries through AI dialogue, abstraction, protocolization, implementation, validation, externalization, and re-entry.

Its purpose is to:

- shorten the time from idea to implementation;
- extract reusable knowledge from AI-assisted dialogue;
- use AI as a development environment, not merely as a code generator;
- accumulate development processes as reusable Protocols; and
- enable rapid development across multiple AI models and environments, including for a solo developer.

## Core Roles

### Human — Direction

The human:

- identifies problems, discomfort, and discoveries;
- establishes purpose and direction; and
- makes the final judgment.

### AI — Expansion and Structuring

AI supports:

- expansion;
- structuring;
- criticism;
- design;
- implementation support; and
- comparison with prior results.

### Protocol — Externalized Context

A Protocol:

- extracts reusable meaning from development activity;
- fixes decisions, principles, and heuristics;
- makes context shareable across AI systems; and
- supports handoff between development sessions and environments.

### Repository — Persistent Development Memory

The repository preserves:

- artifacts;
- history;
- genealogy; and
- the persistent state that can be referred to by subsequent AI-assisted development.

## Development Loop

1. **Observation** — A human presents a problem, discomfort, or discovery.
2. **Dialogue** — AI dialogue expands the observation and exposes possible structure.
3. **Abstraction** — Generalizable structure is extracted.
4. **Protocolization** — Decisions, principles, or heuristics are fixed as Protocol, YAML, or Spec.
5. **Implementation** — The resulting context is converted into implementation, API, UI, Runtime behavior, or related artifacts.
6. **Validation** — The implementation is tested in real environments, with other AI systems/models, or against relevant data.
7. **Externalization** — Validated artifacts and relevant context are stored in a persistent repository such as GitHub.
8. **Re-entry** — Externalized artifacts are returned to subsequent dialogue and design as context.
9. **Iteration** — New discoveries enter the next cycle.

## Canonical Flow

```text
Human Observation
        ↓
   AI Dialogue
        ↓
    Abstraction
        ↓
     Protocol
        ↓
  Implementation
        ↓
    Validation
        ↓
   Repository
        ↓
 Context Re-entry
        ↓
 Next Discovery
```

## Development Unit

SDL treats the primary unit of development as a **Contextual Discovery**, rather than only as a Feature.

The transformation is:

```text
Discovery → Protocol → Implementation → Evidence → New Context
```

This allows development activity itself to become reusable context.

## Difference from Code-First Development

A conventional code-first flow can be represented as:

```text
Idea → Code → Documentation
```

SDL instead uses:

```text
Observation → Meaning → Protocol → Implementation → Context
```

The intention is not to replace ordinary software engineering practices, but to externalize the contextual decisions that would otherwise remain inside conversations, individual memory, or fragmented documentation.

## Multi-AI Development

SDL permits different AI systems or sessions to perform different functions while sharing the same externalized context.

Example roles:

- AI 1 — Ideation
- AI 2 — Criticism
- AI 3 — Implementation
- AI 4 — Research
- Repository — Shared Context

The role assignment is operational, not a requirement that any particular model or vendor be used.

## Acceleration Hypothesis

SDL's working hypothesis is that development bottlenecks are not limited to code-generation speed.

Significant cost can arise from converting discoveries into structure, decisions, and shareable context.

SDL attempts to reduce that conversion cost by structuring discoveries during dialogue and externalizing reusable context continuously.

## Context Layers

SDL distinguishes the following:

- **Transcript** — raw conversational evidence.
- **Memory** — information retained for future use.
- **Protocol** — reusable context that can guide subsequent judgment or execution.
- **Repository** — persistent external context and artifact history.

Not everything needs to be remembered. The objective is to retain the meaning necessary for the next judgment as reusable context.

## Validation Principle

Validation is not limited to determining whether code executes successfully.

A validation cycle should transform a development discovery into observable evidence where possible, preserving the distinction between:

- implementation state;
- observed behavior;
- evidence; and
- subsequent interpretation.

## Relationship to Shirakami OS Document Hierarchy

SDL is a **development method**, not a replacement for the Shirakami OS document hierarchy.

The document hierarchy separates responsibilities vertically:

```text
Vision
  ↓
Constitution
  ↓
Blueprint
  ↓
Design
  ↓
Implementation
```

SDL circulates development activity horizontally across those layers:

```text
Observation → Dialogue → Abstraction → Protocolization
      → Implementation → Validation → Externalization → Re-entry
```

SDL therefore complements the hierarchy rather than redefining it.

## Experimental Observations

Current development experience suggests that:

- concepts can be formed rapidly through AI dialogue;
- protocolization can follow closely behind discovery;
- implementation can proceed directly from externalized context;
- artifacts can be reused across different AI systems and sessions; and
- GitHub can function as persistent external development memory.

These observations remain experimental and should be validated through continued use.

## Possible Future Components

The following are possible implementation directions, not current requirements:

- SDL Runner
- Protocol Compiler
- Context Diff
- AI Role Router
- Evidence Ledger
- Development Genealogy
- Multi-Agent Development Runtime

They should not be treated as part of the current Shirakami OS implementation unless separately adopted through the project's formal handoff process.

## One-Line Definition

> Shirakami Development Loop is a context-circulating development method that structures human discoveries through AI dialogue, externalizes them as Protocol, implements and validates them, then returns them to the next discovery.

## Status

This document is **Experimental / v0.1**.

It records the development method currently being used around Shirakami OS. Further theoretical changes should be handled through the research process and formally handed off before being adopted as project requirements.

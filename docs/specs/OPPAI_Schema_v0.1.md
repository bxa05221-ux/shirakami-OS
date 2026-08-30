# OPPAI Schema v0.1

**Operating Prompt Protocol for AI Schema**

Status: experimental implementation

## Purpose

OPPAI defines a preprocessing boundary between ordinary human interaction and downstream AI execution.

The user is not required to write machine-optimized prompts. OPPAI observes natural language first, preserves the conversational sequence, and exposes structured signals without prematurely deciding hidden intent.

## Core principle

> The human should be allowed to operate the AI naturally; the system should absorb appropriate interpretation work.

## Separation rules

- raw human input MUST be preserved.
- explicit corrections MUST be observable and MUST NOT erase preceding context.
- unresolved questions MUST remain unresolved.
- interaction signals such as positive affirmation MUST NOT be treated as factual validation.
- canonicalization MUST NOT silently invent hidden intent.
- downstream model choice remains replaceable.

## Minimal pipeline

```text
Human Input
    ↓
Raw Preservation
    ↓
Segmentation
    ↓
Correction / Interaction / Uncertainty Signals
    ↓
Canonical Prompt Candidate
    ↓
Downstream AI Adapter
```

## Current implementation boundary

The v0.1 implementation is intentionally dependency-light and deterministic. It does not call an LLM. It provides an observable preprocessing object and a Runtime API endpoint.

Endpoint:

`POST /v0.1/oppai/normalize`

Input:

```json
{"text":"...", "context": {}}
```

Output contains:

- `raw_input`
- `segments`
- `corrections`
- `interaction_signals`
- `unresolved`
- `canonical_prompt`
- `confidence`

## Non-goals

OPPAI v0.1 does not claim to understand the user's hidden psychological state, determine truth, resolve all references, or guarantee downstream answer quality.

## Relationship to Shirakami OS

OPPAI is an input-boundary component. It is not the OS itself and does not replace Protocol, Evidence, Permission, Landscape, or Human Decision layers.

Its role is to make natural human interaction available to those layers without requiring machine-oriented prompt authoring by the human.

## Evidence target

Future implementation should observe whether OPPAI reduces:

- correction turns
- re-explanation turns
- context recovery
- human prompt-editing effort
- time spent repairing AI misunderstandings

These are measurement targets, not claims of demonstrated improvement.

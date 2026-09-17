# README Entry Proposal v1

This document defines the proposed first-time entry structure for Shirakami OS.

## 30-second explanation

> **Shirakami OS is a runtime for working with human context even when AI systems change.**

Shirakami OS is not an LLM and not an AI agent. It is an open-source, protocol-driven runtime architecture for preserving, observing, and reconstructing human context across AI systems and backends.

```text
Landscape
   ↓
Protocol
   ↓
Runtime
   ↓
Evidence
   ↓
Landscape State
```

## What the current prototype demonstrates

- A minimal executable Runtime boundary
- Protocol-shaped execution
- Observable transitions
- Evidence capture from execution results
- Landscape State updates
- A local path that does not require an external AI provider

The prototype is an implementation proof. It is not a claim that the complete Shirakami architecture is finished.

## Start here

### Technical entry

```bash
python shirakami_os.py
```

This runs the smallest executable OS boundary: boot Landscape, execute a Protocol, capture an observable transition, record Evidence, and expose the resulting Landscape State.

For the broader verification route, see:

- [MVP Quickstart](MVP_QUICKSTART.md)
- [Reviewer Entry Point](REVIEWER_ENTRY_POINT.md)
- [Local Quickstart](../../examples/quickstart/README.md)

### Experience entry

[Thread RPG](../../products/thread-rpg-v1.2.1/) is the public-facing experience artifact for exploring Protocol-driven interaction and human-observable dialogue structure.

The technical Runtime prototype and the Thread RPG experience should be understood as related but distinct entry points.

## Scope boundary

The current prototype does not claim to provide complete cross-provider memory or personality transfer. Such capabilities remain future work unless demonstrated by an executable implementation and corresponding evidence.

## Review focus

Reviewers are invited to examine:

- Architecture boundaries
- Protocol semantics
- Runtime behavior
- Evidence integrity
- Landscape State handling
- Adapter and backend separation
- Security and failure handling
- First-time usability

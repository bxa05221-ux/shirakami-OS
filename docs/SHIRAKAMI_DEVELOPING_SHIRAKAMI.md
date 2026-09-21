# Shirakami Developing Shirakami

## Purpose

This document records a defining characteristic of the Shirakami project:
**Shirakami is developed through the same externalization, protocol, evidence, and verification principles that it implements.**

This is not a claim of autonomous self-development. Human judgment remains the final authority. AI is used as a support and simulation layer, while decisions, approvals, merges, and acceptance remain externally attributable.

## The Self-Referential Development Loop

```text
Human observation / problem
        ↓
Conversation and exploration
        ↓
Externalization into protocol, schema, or specification
        ↓
Implementation in the Runtime / API / adapter boundary
        ↓
Tests, CI, and observable results
        ↓
Evidence, diff, and documented residue
        ↓
Human review and acceptance
        ↓
Reuse as the next development context
        ↺
```

The project therefore has two simultaneous layers:

1. **The product layer** — Shirakami provides boundaries for evidence-driven, human-authorized AI interaction.
2. **The development layer** — the project itself uses those boundaries as a method for making design decisions, implementation changes, and verification results explicit.

## What Is Actually Being Demonstrated

The repository does not claim that every internal AI influence can be extracted or that the system modifies itself without authorization. The demonstrated boundary is narrower and testable:

- assumptions can be externalized;
- candidate protocols can be separated from approved protocols;
- human authorization can be made explicit;
- execution can be addressed through observable handles;
- verification can preserve expected and observed results separately;
- mismatches can become reusable Evidence;
- implementation history can remain inspectable through specifications, commits, pull requests, tests, and CI.

## Why This Matters

A conventional project may describe its design first and implement it afterward. Shirakami also treats the development process as an experimental Landscape. Each cycle produces artifacts that can become inputs to later cycles.

This creates a practical form of self-reference:

> Shirakami is not only being built as a protocol/runtime framework; its own development is a continuing test of whether externalized context, human gates, Evidence, and verification can support real work.

The loop is **self-referential, not self-authorizing**.

## Evidence Boundary

The following artifacts are part of the inspectable development record:

- specification changes in `shirakami-specification`;
- implementation changes in `shirakami-OS`;
- pull requests and review decisions;
- automated test and CI results;
- execution records and verification results where available;
- documented mismatches, limitations, and unresolved boundaries.

These artifacts do not prove that the system is complete. They show where a claim is supported, where it remains provisional, and what the next verification boundary should be.

## Core Statement

> **白神は、白神を開発する過程そのものを、白神の原理で外部化・検証している。**

English:

> **Shirakami is developed through the same principles of externalization, human authorization, evidence, and verification that it is designed to provide.**

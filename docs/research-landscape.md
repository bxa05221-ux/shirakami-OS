# Research Landscape & Related Work

Shirakami OS does not claim to replace existing AI interoperability, memory, continuity, or agent frameworks.

This document records adjacent open-source projects and research directions that are relevant to the problem space. The purpose is to make the project's position inspectable and to invite comparison, review, and collaboration.

## 1. Agent interoperability

### A2A — Agent2Agent Protocol
https://github.com/a2aproject/A2A

Focus: Agent-to-agent communication and collaboration.

Relation to Shirakami OS: adjacent. A2A addresses interoperability between agents; Shirakami OS focuses on the persistence, observation, protocolization, and runtime handling of human Landscape across replaceable AI systems.

### MCP — Model Context Protocol
https://github.com/modelcontextprotocol

Focus: standardized access to tools, resources, and context.

Relation to Shirakami OS: adjacent and potentially complementary. Shirakami OS does not position itself as an MCP replacement. MCP can serve as an adapter/integration boundary within a Shirakami runtime.

## 2. Human Context

### Human Context Protocol (HCP)
https://github.com/human-context-protocol/hcp

Focus: a protocol direction for portable human context between LLM clients and memory/context infrastructure.

Relation to Shirakami OS: closely related. Both treat human-owned context as something that should remain usable across changing AI systems. Shirakami OS additionally models Landscape, Evidence, Protocol, Runtime, and Observation as an implementation flow.

Note: repository identity and scope should be re-checked before making claims about formal institutional affiliation or maturity.

## 3. Portable AI / Agent Memory

### Portable Agent Memory
https://github.com/santhoshravindran7/portable-agent-memory

Focus: portability of persistent agent memory across systems.

Relation to Shirakami OS: closely related to the AI/model portability problem. Shirakami OS treats memory as one component of a broader Landscape rather than the complete system boundary.

### context-use
https://github.com/onfabric/context-use

Focus: importing and using context/data from AI systems in a portable workflow.

Relation to Shirakami OS: adjacent implementation work around portable context and AI interoperability.

## 4. AI Continuity and Evaluation

### ATANT / Kenotic Labs
https://github.com/Kenotic-Labs/ATANT

Focus: evaluation of AI continuity characteristics such as persistence, update handling, temporal ordering, disambiguation, reconstruction, model independence, and operational usefulness.

Relation to Shirakami OS: potentially complementary. ATANT is useful as an external evaluation perspective for continuity; Shirakami OS is an implementation architecture for Landscape, Evidence, Protocol, Runtime, and observation.

Status note: if the repository is unavailable or its ownership/scope cannot be independently verified, this entry should remain marked as a research lead rather than treated as an authoritative reference.

## 5. Memory infrastructure and contracts

### MemTools

Focus: structured memory handling and data-contract-oriented agent memory infrastructure.

Relation to Shirakami OS: adjacent. It is relevant to the separation of memory representation and execution/runtime concerns.

The exact repository/reference should be added only after verification of the canonical upstream project.

## Position of Shirakami OS

The current working position is:

```text
Human Landscape
       ↓
Evidence
       ↓
Protocol
       ↓
Runtime
       ↓
Adapter
       ↓
AI / Agent / External System
```

This should not be read as a claim that surrounding projects occupy no part of these layers. The purpose is to describe the architectural emphasis currently being explored by Shirakami OS.

## Comparison rule

When adding related work:

1. Prefer canonical upstream repositories or institutional research pages.
2. Verify the repository and project identity before describing it as an established reference.
3. Separate source-derived facts from Shirakami OS interpretation.
4. Do not describe adjacent projects as competitors unless the evidence supports that claim.
5. Do not claim novelty merely because a similar implementation was not found.
6. Use related work to define boundaries, integration opportunities, and unanswered questions.

## Research question

A central question for Shirakami OS is:

> How should a runtime preserve and carry forward human Landscape when the underlying AI model, agent, or vendor is replaceable?

The project invites comparison with work on human context, portable memory, AI continuity, agent interoperability, governance, and runtime infrastructure.

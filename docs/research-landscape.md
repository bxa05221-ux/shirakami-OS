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

## 6. Shirakami Cognitive Observation Architecture

Shirakami OS also contains a distinct line of work concerned not only with storing context, but with observing how a human Landscape changes as the cognitive position changes.

### Celestial Model

Role: cognitive space.

Question: what cognitive space is currently being observed, what is within view, and what remains outside the current field of view?

### 3D Phase-Rotating Eisenhower Matrix

Role: cognitive position and phase rotation.

Purpose: change the cognitive position from which the same Landscape is observed. The position is not treated as fixed, and priority may change with phase and perspective.

### Cognitive Echolocation

Role: cognitive observation.

Purpose: observe changes, newly observable relations, gaps, and hidden questions from the current cognitive position.

### Anmon Layer

Role: unresolved-question layer.

Purpose: retain questions that have not yet been resolved without forcing premature interpretation or closure.

### AASS

Role: observation-to-operation connection.

Status: definition and formal relationship should follow the existing AASS protocol rather than being expanded here without research feedback.

### Architecture

```text
Human Landscape
       ↓
Celestial Model
       ↓
3D Phase-Rotating Eisenhower Matrix
       ↓
Cognitive Echolocation
       ↓
Evidence
       ↓
Anmon Layer / unresolved questions
       ↓
Protocol
       ↓
Runtime
       ↓
AASS / operational connection
       ↓
Adapter
       ↓
AI / Agent / External System
```

This layer is an architectural exploration, not a claim that the individual concepts are universally novel or uniquely implemented by Shirakami OS.

## 7. Thread RPG lineage

The Shirakami AA Thread Simulator Lite is an early conversational prototype that predates and led toward the Thread RPG line of work.

### Shirakami AA Thread Simulator Lite

The Lite protocol treats AA and kaomoji as an emotional/temperature UI and explicitly includes:

- input organization
- AA emotion temperature
- ambiguity preservation
- cooling responses
- silence avoidance

Its core rule is not to over-infer: ambiguous input remains unresolved, possible interpretations may be presented, and the conversation should continue without premature certainty.

The prototype is therefore relevant to the later cognitive-observation architecture as an early test of observable conversational temperature, ambiguity preservation, and continuity.

### Lineage

```text
Shirakami AA Thread Simulator Lite
              ↓
          Thread RPG
              ↓
   Cognitive Observation
              ↓
 Shirakami Cognitive Observation
        Architecture
```

The lineage should be understood as a project-development path, not as a claim that Thread RPG has only one source or that all later concepts are already fully implemented in the Lite protocol.

## Position of Shirakami OS

The current working position is:

```text
Human Landscape
       ↓
Cognitive Observation
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
7. Do not expand or redefine an existing Shirakami protocol merely to make it fit the landscape document.

## Research question

A central question for Shirakami OS is:

> How should a runtime preserve and carry forward human Landscape when the underlying AI model, agent, or vendor is replaceable?

A second question is:

> How can a runtime observe changes in a human Landscape and changes in cognitive position without reducing the person to an AI-generated interpretation?

The project invites comparison with work on human context, portable memory, AI continuity, agent interoperability, governance, runtime infrastructure, and cognitive observation.

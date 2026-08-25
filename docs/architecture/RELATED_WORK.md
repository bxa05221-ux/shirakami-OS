# Related Work / Comparative Landscape

## Purpose

This document maps adjacent research and open-source implementations around memory, context management, stateful agents, and AI runtime design.

It is **not a competitor list** and does not claim that Shirakami OS is unique in every mechanism.

The purpose is to make the surrounding landscape visible and to identify where Shirakami overlaps, differs, or may be tested against existing work.

## Comparison axis

Shirakami uses the following working distinction when reviewing related systems:

1. **AI-self-declared / model-centric design** — the architecture primarily starts from what an AI agent needs in order to reason, remember, retrieve, or act.
2. **Human-operational / landscape-centric design** — the architecture primarily emerges from sustained human use, observed limitations, and the need to preserve a human-owned context across models or sessions.

This is an analytical axis, not a value judgment. A project may contain elements of both.

## Current reference points

### Letta / MemGPT

Official repository: https://github.com/letta-ai/letta

Letta describes itself as an open-source framework for stateful LLM applications with advanced reasoning and long-term memory, and is model-agnostic.

**Overlap with Shirakami**

- Stateful AI operation
- Long-term memory
- Model independence
- Runtime/application boundary

**Difference to investigate**

Shirakami places the human-owned **Landscape** outside the model and treats Protocol and Evidence as first-class architectural boundaries. The comparison should therefore focus on whether the persistent state is primarily an agent memory system or a portable human context/landscape system.

### A-MEM / Agentic Memory

Official implementation: https://github.com/WujiangXu/A-mem-sys

A-MEM describes an agentic memory system that dynamically organizes memories, creates structured notes and links, and evolves memory through connections between past experiences.

**Overlap with Shirakami**

- Structured memory
- Dynamic organization
- Linking of historical information
- Reducing dependence on raw historical context

**Difference to investigate**

A-MEM is primarily a memory architecture for agents. Shirakami treats memory as one domain within a broader Landscape containing Identity, Personality, Knowledge, Projects, Skills, Protocols, Permissions, and Evidence.

### Context-management / compression research

Representative research includes ACON and other systems that reduce the amount of context presented to long-running agents while attempting to preserve task performance.

**Overlap with Shirakami**

- Avoiding unnecessary historical context
- Reducing context/token load
- Preserving task-relevant state

**Difference to investigate**

Shirakami does not define its core mechanism as generic context compression. The working hypothesis is that **externalizing conversational state into Thread, Anmon Layer, Matome YAML, and Landscape can reduce the need to repeatedly reconstruct the same context**.

That hypothesis requires direct measurement rather than assumption.

## Shirakami-specific observation targets

The following should be tested against related systems rather than asserted as established superiority:

- Whether Thread externalization reduces repeated context transmission.
- Whether Anmon Layer reduces the need to resolve or restate unresolved questions.
- Whether Matome YAML provides more portable context than model-specific memory.
- Whether Thread RPG can function as a lightweight human-readable state interface.
- Whether a lighter model can perform a task adequately when Landscape and Protocol structure reduce the reasoning/context burden.
- Whether model/vendor changes preserve the human-owned Landscape with less migration effort.

## Important distinction: mechanism vs origin

Similar mechanisms are expected to converge across the field. Memory, retrieval, context compression, state management, and agent runtimes are natural engineering responses to the limits of long-context AI systems.

The more important Shirakami research question is therefore not:

> "Did Shirakami invent this mechanism first?"

It is:

> "Did the mechanism emerge from sustained human-AI operation, and does that operational origin produce a useful architectural difference?"

## Experimental direction

Future comparisons should record observable evidence where possible:

- input tokens
- output tokens
- total tokens
- context size
- number of retrieval/tool calls
- task success
- context-loss events
- recovery/re-explanation events
- model changes
- portability/migration effort

A particularly relevant experiment is:

```text
Same task / same Landscape

A. Raw conversation history
B. Conventional summary memory
C. Anmon Layer
D. Thread RPG
E. Anmon Layer + Thread RPG

Compare token use, task success, recovery cost, and context continuity.
```

## Position

Shirakami should link to adjacent projects openly, credit their work, and treat them as part of the research landscape.

The objective is not to prove that Shirakami is isolated from existing research. The objective is to make the boundary between **model capability**, **memory architecture**, **runtime architecture**, and **human-owned Landscape** observable.

---
applyTo: "**/oppai/**,**/*OPPAI*,**/*oppai*"
---

# OPPAI-specific guidance

Treat OPPAI as a draft Human-AI Interaction Protocol within Shirakami OS.

## Preserve the current boundary

OPPAI is not Shirakami OS, not an LLM, not a Runtime, not a domain expert engine, and not a decision authority.

Its purpose is to describe how the system can receive and preserve natural human thought flow as a signal while maintaining the existing Shirakami boundaries.

## Current responsibility model

- Listener
- Context Preservation
- Intent Separation
- Clarification
- Canonicalization
- Execution
- Evidence

Do not assume that these seven responsibilities are seven fixed runtime layers. Their ordering and internal mechanics remain experimental.

## Conversation and ambiguity

Do not force the human to reformulate natural thought merely to satisfy an AI task format.

When ambiguity exists, preserve useful context and clarify only as needed. Do not prematurely collapse uncertain intent into a single interpretation.

Keep inference separate from fact. Observable transitions belong to Evidence.

## 暗問層

Treat 暗問層 as a cross-cutting safeguard for unresolved questions and premature semantic fixation. Do not implement it as a mandatory eighth OPPAI layer unless an explicit future specification says so.

## Implementation rule

If a proposed implementation requires changing the meaning or constitutional boundary of OPPAI, stop treating it as ordinary implementation work. Record the discrepancy and route it back to the research/specification boundary.

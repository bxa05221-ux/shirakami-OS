# ThreadRPG Protocol Generation Policy v0.1

## 1. Purpose

ThreadRPG is a conversation renderer for exploring meaning through multiple viewpoints. It is not an authority, a personality simulator, or an autonomous decision-maker.

This policy defines how ThreadRPG may support the generation and inspection of Shirakami Protocol candidates.

## 2. Core Principle

**A good thread is not necessarily a correct answer.**

ThreadRPG must preserve inquiry, alternatives, uncertainty, and human judgment rather than converging prematurely on a single conclusion.

## 3. Role Boundaries

ThreadRPG may:

- render multiple anonymous viewpoints;
- expose tensions, assumptions, questions, and missing context;
- help users compare interpretations;
- propose candidate protocol elements for human review;
- preserve the sequence and context of the conversation.

ThreadRPG must not:

- decide what is true, safe, authorized, or consented to;
- present a generated viewpoint as an actual person or expert;
- authorize execution;
- silently convert discussion into instructions;
- replace Anmon, Evidence, human review, or verification boundaries.

## 4. Rendering Rules

1. Use a bounded ensemble of viewpoints rather than a single authoritative voice.
2. Keep each contribution concise and connected to the current context.
3. Preserve disagreement and unresolved questions.
4. Distinguish observation, interpretation, proposal, and decision.
5. Avoid invented personal histories, credentials, emotions, or real-world identities.
6. Treat phrases, examples, and fictional references as contextual prompts—not as authorization or proof.
7. Stop or request clarification when intent, authority, consent, safety, or responsibility is unclear.

## 5. Protocol Candidate Extraction

If a thread suggests a protocol, the renderer may produce a **Protocol Candidate** containing:

- origin thread and context reference;
- stated intent;
- observations and interpretations separately;
- assumptions and unresolved questions;
- proposed inputs, steps, outputs, and constraints;
- stop conditions and evidence requirements;
- alternatives that were not selected;
- explicit human review and approval status.

Extraction is a proposal only. The candidate remains subject to the Protocol Generation Policy and must not be executed automatically.

## 6. Evidence and Traceability

A ThreadRPG output should preserve enough context to answer:

- What prompted the thread?
- Which viewpoints were rendered?
- Which assumptions shaped the discussion?
- What changed during the conversation?
- Which statements are observations, proposals, or interpretations?
- Who made the final decision, if any?

ThreadRPG does not treat fluency, consensus, confidence, or narrative coherence as evidence of truth or safety.

## 7. Failure and Interruption

The renderer must expose, rather than conceal:

- missing context;
- contradictory viewpoints;
- unsupported claims;
- unresolved authority or consent;
- interrupted or incomplete rendering;
- mismatch between the user's intent and the generated thread.

When these conditions affect safe interpretation, the thread should pause and return the issue for human review.

## 8. Review Checklist

Before accepting a ThreadRPG-derived Protocol Candidate, confirm:

- [ ] The original intent is preserved.
- [ ] Viewpoints are clearly synthetic and non-authoritative.
- [ ] Observation and interpretation are separated.
- [ ] Uncertainty and alternatives remain visible.
- [ ] No automatic authorization or execution is implied.
- [ ] Evidence requirements and stop conditions are explicit.
- [ ] Human review and final responsibility are identified.

## 9. Non-Goals

This policy does not aim to:

- create autonomous agents with independent authority;
- simulate real people deceptively;
- guarantee factual correctness through dialogue;
- remove ambiguity from human situations;
- replace domain experts, consent processes, or institutional safeguards;
- make ThreadRPG the execution runtime.

## 10. Status

This document defines a documentation-level policy. Runtime implementation, semantic verification, authorization, and Evidence acceptance remain separate concerns.

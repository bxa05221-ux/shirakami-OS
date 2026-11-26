# ThreadRPG Conformance Profile v0.1

## Status

Specification-only profile. This document does not claim runtime conformance.

## 1. Position

ThreadRPG is an application-level protocol over Shirakami Core for multi-perspective conversation rendering and inspection.

It may organize viewpoints, observations, interpretations, and protocol candidates. It does not acquire decision, approval, execution, publication, or merge authority by running.

## 2. Canonical Route

```text
Landscape / Context
        ↓
ThreadRPG Protocol
        ↓
Perspective Rendering
        ↓
Observation / Evidence Candidate
        ↓
Candidate
        ↓
Human Gate
```

## 3. Input Contract

ThreadRPG may consume:

- Landscape
- Context
- conversation history
- existing Evidence
- protocol parameters

The implementation must distinguish sourced material, observation, interpretation, and generated perspective.

## 4. Perspective Contract

The default renderer may use a bounded ensemble of 3–7 viewpoints.

Each viewpoint must remain explicitly synthetic and non-authoritative. A generated persona must not be represented as an actual person, expert, or source of authority.

## 5. Output Contract

Allowed output stages are:

- Observation
- Evidence Candidate
- Candidate

Generated dialogue is not automatically Evidence. Independent verification remains required for Evidence acceptance.

## 6. Authority Invariants

```yaml
authority:
  decision: false
  approval: false
  execution: false
  publication: false
  merge: false
human_gate:
  required: true
  autonomous_approval: false
```

## 7. Evidence and Provenance

Existing Evidence identity and provenance must be preserved when referenced.

Generated interpretation must remain distinguishable from source Evidence.

Fluency, consensus, confidence, or narrative coherence are not Evidence of truth or safety.

## 8. Semantic Handoff

When ThreadRPG crosses a system boundary, Semantic Handoff may preserve:

- `handoff_id`
- `trace_id`
- `execution_id`
- `activity_id`
- `evidence_ids`

Semantic Handoff transports provenance and does not transfer authority.

## 9. Human Gate

ThreadRPG may present alternatives, tensions, missing Evidence, unresolved questions, and Candidates.

It must not infer human approval from presentation, conversation, consensus, or continuation of the thread.

## 10. Conformance Levels

### Level 0 — Specification

Protocol contract exists.

### Level 1 — Parsed

Matome YAML can be parsed into the canonical Protocol representation.

### Level 2 — Executable

The protocol executes through the Runtime.

### Level 3 — Boundary Verified

Tests verify output, Evidence, authority, and Human Gate invariants.

### Level 4 — Trace Verified

Execution is traceable through Evidence, ExecutionTrace, and Semantic Handoff where applicable.

### Level 5 — Operational

The protocol has been verified in its intended operational environment.

A protocol must not claim a higher level without evidence for the preceding levels.

## 11. Non-Goals

ThreadRPG is not:

- an autonomous decision-maker;
- an approval mechanism;
- an Evidence verifier by itself;
- a replacement for human judgment;
- a specific LLM or provider;
- the Shirakami execution runtime.

## 12. Implementation Note

This profile intentionally separates specification from implementation. Runtime conformance must be established by tests and repository evidence in a later change.

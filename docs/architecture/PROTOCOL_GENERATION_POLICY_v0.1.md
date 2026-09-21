# Shirakami Protocol Generation Policy v0.1

## Purpose

This document defines the design policy for Protocols generated or proposed within Shirakami.
The objective is not to maximize autonomous generation, but to improve **prompt precision, traceability, human control, and reproducibility**.

## Core Principle

> A generated Protocol is a candidate for human inspection, not an authority for execution.

AI may propose structure, alternatives, transformations, and questions. It must not silently convert a proposal into an approved operational rule.

## Generation Boundaries

Every Protocol candidate SHOULD distinguish the following layers:

1. **Origin** — the observed need, question, problem, or triggering context.
2. **Intent** — what the human or system is trying to achieve.
3. **Assumptions** — premises used during generation, including uncertainty.
4. **Protocol Structure** — inputs, steps, outputs, constraints, and stop conditions.
5. **Execution Conditions** — prerequisites and explicit approval requirements.
6. **Evidence Plan** — what will be recorded during and after execution.
7. **Evaluation Boundary** — what remains for human judgment or external verification.

## Mandatory Separation

### 1. Inspiration vs. Implementation

The source of an idea and its implementation proposal MUST be recorded separately.

- **Inspiration path:** why the idea emerged and from which observations or associations.
- **Implementation design:** how the idea could be represented, tested, executed, or rejected.

A plausible implementation MUST NOT be treated as proof that the original idea is valid.

### 2. Execution vs. Verification

Execution records what the Runtime did.
Verification evaluates what the result means or whether it satisfies the intended criteria.

A completed execution MUST NOT automatically become verified, accepted, or promoted Evidence.

### 3. Candidate vs. Authorization

Protocol generation may produce a candidate route or structure.
Authorization requires an explicit human gate or another explicitly declared governance mechanism.

### 4. Observation vs. Interpretation

Observable events, interpretations, and conclusions MUST remain distinguishable.
Uncertainty MUST NOT be silently converted into fact.

## Required Candidate Fields

A Protocol candidate SHOULD expose, at minimum:

```yaml
protocol_candidate:
  id: "..."
  version: "..."
  origin:
    observations: []
    question: "..."
  intent:
    objective: "..."
    human_owner: "..."
  assumptions: []
  inputs: []
  steps: []
  outputs: []
  constraints: []
  stop_conditions: []
  evidence_plan:
    execution_events: []
    expected_observations: []
    mismatch_handling: "..."
  approval:
    required: true
    gate: "HUMAN_REVIEW"
  verification:
    separate_from_execution: true
    evaluator: "..."
  status: "CANDIDATE"
```

The schema is illustrative rather than a claim that every field is already implemented by the Runtime.

## Generation Rules

- Prefer the smallest useful Protocol that can be inspected and tested.
- State what the Protocol does **not** decide.
- Preserve alternative candidates rather than collapsing uncertainty prematurely.
- Do not infer semantic compatibility from structural similarity alone.
- Do not infer truth, safety, consent, or authorization from model confidence.
- Make assumptions and missing information visible.
- Include failure, interruption, and mismatch paths.
- Keep provider-specific behavior inside adapters or explicitly declared boundaries.
- Preserve the original human intent even when the generated structure changes.
- Treat generated text, diagrams, and code as representations that require review.

## Review Checklist

Before a candidate is promoted for execution, reviewers SHOULD ask:

1. Is the origin of the Protocol clear?
2. Is the intended human outcome explicit?
3. Are assumptions separated from observations?
4. Are inputs and outputs testable?
5. Are stop conditions defined?
6. Is human authorization explicit?
7. Can execution be distinguished from verification?
8. Is the Evidence plan sufficient to reconstruct what happened?
9. What could drift from the original intent?
10. What remains unknown or outside the Protocol's authority?

## Status Vocabulary

- `IDEA` — an unstructured possibility.
- `CANDIDATE` — a structured proposal awaiting review.
- `REVIEWED` — inspected by a human, with review notes preserved.
- `READY` — explicitly authorized for execution.
- `EXECUTED` — operational execution completed or interrupted and recorded.
- `VERIFIED` — evaluated against declared criteria.
- `ACCEPTED` — explicitly adopted by the responsible human or governance process.
- `REJECTED` — not adopted; the reason may be preserved as Evidence.
- `SUPERSEDED` — replaced by a later version without rewriting the historical record.

These statuses MUST NOT be treated as interchangeable.

## Non-Goals

This policy does not attempt to:

- make AI the final decision-maker;
- infer domain truth from language-model output;
- guarantee semantic compatibility automatically;
- eliminate human responsibility;
- require a single model, vendor, or backend;
- claim that every Protocol can be freely composed with every other Protocol.

## Design Direction

Shirakami should become better at generating **inspectable Protocol candidates**, not at bypassing human judgment.

The target is a system in which every generated Protocol can answer:

> Where did this come from, what does it intend, what does it assume, what will it do, what will it record, and who decides whether it is accepted?

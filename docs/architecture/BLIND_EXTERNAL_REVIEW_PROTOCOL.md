# Shirakami OS — Blind External Review Protocol

## Purpose

This protocol defines a repeatable method for obtaining an independent external observation of the repository architecture without giving the reviewer the project's expected conclusion.

The protocol is intended for human reviewers or external AI reviewers.

It is an observation protocol, not a certification procedure and not a decision mechanism.

## Core rule

The reviewer must begin from the public Reviewer Entry Point:

- `docs/architecture/REVIEWER_ENTRY_POINT.md`

The reviewer should not be given:

- prior reviewer conclusions;
- expected interpretations;
- internal explanations of why the architecture is designed a certain way;
- instructions to confirm a particular architectural claim.

The reviewer may be given only the review objective, the repository reference, and the required output boundary.

## Review sequence

```text
Reviewer Entry Point
        ↓
Independent repository inspection
        ↓
Observed facts
        ↓
Evidence references
        ↓
Interpretation
        ↓
Questions / unresolved points
        ↓
Falsifiable points
        ↓
Human Gate
```

The reviewer must preserve the distinction between each stage.

## Required output

An external reviewer should return a Matome YAML containing:

- reviewer identity;
- review objective;
- observations;
- evidence references;
- resolved questions;
- unresolved questions;
- falsifiable points;
- proposals;
- interpretation;
- Human Gate state.

The reviewer must not emit a decision on behalf of the project.

## Observation boundary

The reviewer may inspect and report:

- repository structure;
- implementation;
- tests;
- specifications;
- documented architecture;
- execution paths;
- authority-boundary fields;
- Evidence references;
- inconsistencies;
- missing verification;
- questions raised by the implementation.

The reviewer must not:

- grant execution authority;
- grant publication authority;
- grant merge authority;
- convert a proposal into a decision;
- treat an interpretation as Evidence;
- treat a passing test as proof of the entire architecture;
- silently reconcile contradictory observations.

## Blindness requirement

A review is considered blind only when the reviewer has not been supplied with the expected conclusion before inspection.

The reviewer may discover the documented architecture during the inspection. Discovering the architecture from the repository is part of the observation.

The distinction is:

```text
Expected conclusion supplied before inspection
    → not blind

Architecture discovered from repository evidence
    → blind review remains valid
```

## Re-review protocol

When the architecture changes, a subsequent independent review should:

1. start again from the Reviewer Entry Point;
2. avoid the previous review result;
3. inspect the current repository state;
4. record which previous questions appear resolved;
5. record which questions remain unresolved;
6. record newly discovered questions;
7. identify at least one falsifiable point where practical.

A later review is not automatically evidence that an earlier interpretation was correct.

## Evidence promotion

External review output is initially an observation.

It becomes candidate Evidence only after repository or test verification.

```text
External observation
        ↓
Candidate question
        ↓
Repository / test verification
        ↓
Accepted Evidence
```

The external reviewer therefore cannot establish its own authority merely by producing a structured review.

## Human Gate

The Human Gate remains outside the reviewer pipeline.

```text
Reviewer
   ↓
Comparative Trace
   ↓
AIwitness
   ↓
Traceability
   ↓
Human Gate
   ↓
Human judgment
```

No step before the Human Gate may create decision authority.

## Optional HTTP Submission Route

When an HTTP interface is available, a reviewer may submit the structured result through the repository's blind-review boundary rather than registering and submitting each observation separately.

```text
Matome YAML
    ↓
POST /v1/reviews/blind
    ↓
validation + ReviewerBundle ingestion
    ↓
POST /v1/reviews/blind/comparative/aiwitness
    ↓
comparative traceability validation
```

This route is an implementation convenience, not an authority channel. The API must preserve `decision = null`, `authority_granted = false`, `decision_authorized = false`, and `human_gate_required = true`. A successful HTTP response is evidence about that request path only; it is not a certification of the wider architecture.

## Success condition

The purpose of this protocol is not to make independent reviewers reach the same conclusion.

A successful review process is one in which independent reviewers can:

- reconstruct the implementation boundary;
- distinguish observation from interpretation;
- identify Evidence and its limits;
- preserve disagreement;
- identify unresolved questions;
- identify falsifiable claims;
- leave the final judgment to a human.

Disagreement is therefore a valid review outcome.

## Non-goals

This protocol does not:

- certify Shirakami OS;
- establish production readiness;
- prove semantic correctness;
- replace the normative specification;
- replace automated tests;
- delegate human judgment to reviewers or AI.

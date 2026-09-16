# Shirakami Self-Diagnostic Protocol v0.1

Status: **research-candidate — internal Runtime target**

## 1. Purpose

This protocol defines a self-diagnostic function for observing the current state of Shirakami against an expected state and reporting what can be confirmed, what remains unverified, and where inconsistencies exist.

Self-diagnostic is intended to support verification and handoff. It is not a mechanism for Shirakami to declare that it is correct.

## 2. Core Principle

> Self-Diagnostic observes the state of the system; it does not judge the system to be correct.

The diagnostic result must distinguish observation from evaluation.

Self-Diagnostic MUST NOT be treated as an authority that certifies its own correctness.

## 3. Diagnostic Result Classes

A diagnostic operation may report the following classes:

- `confirmed` — the relevant state or condition was directly verified.
- `unverified` — the expected state could not be established from available verification data.
- `failed` — an expected condition was checked and was not satisfied.
- `incomplete` — the verification process itself is incomplete.
- `inconsistent` — available state information contains a contradiction or mismatch.

These classes describe verification state. They are not quality scores or overall judgments.

## 4. Evidence Boundary

The intended information flow is:

```text
Observation
    ↓
Evidence
    ↓
Self-Diagnostic
    ↓
Diagnostic Result
```

Self-Diagnostic MUST NOT manufacture Evidence merely to prove its own result.

A diagnostic result may refer to existing Evidence, verification output, repository state, test results, or other observable state, but it must preserve the distinction between observed facts and diagnostic interpretation.

## 5. Submission Check as an Application

The Submission Check Protocol is treated as an application of Self-Diagnostic.

The minimum submission-state sequence is:

```text
Changed
  ↓
Tested
  ↓
Reviewed
  ↓
Submitted
  ↓
Merged
  ↓
Canonicalized
  ↓
Post-verified
```

A change MUST NOT be declared complete merely because its implementation tests pass.

Submission Check additionally verifies the delivery target and repository state.

## 6. Diagnostic Scope

The initial internal diagnostic scope is:

- State Diagnostic
- Verification Diagnostic
- Submission Diagnostic
- Canonical Diagnostic
- Evidence Diagnostic

This scope is intentionally limited. It does not introduce a general-purpose AI judgment layer.

## 7. API Boundary

Self-Diagnostic is an internal Runtime target in this version.

It does **not** add a new external API endpoint to the β1.0 contract.

The current frozen external boundary remains:

```text
POST /observe
```

Any future external exposure of diagnostic information requires a separate API-boundary decision, implementation, process-boundary verification, review, and contract freeze.

Runtime capability MUST NOT automatically become an external API merely because the capability exists internally.

## 8. Ownership

### Research

Research owns:

- the meaning of Self-Diagnostic;
- diagnostic result classes;
- the distinction between observation and judgment;
- the Evidence relationship;
- the boundary between internal diagnostic capability and external API exposure.

### Runtime

Runtime owns:

- acquisition of observable state;
- inspection and comparison mechanisms;
- diagnostic processing;
- implementation tests;
- reporting of diagnostic state without changing the underlying theory.

Runtime MUST NOT expand the theoretical meaning of Self-Diagnostic during implementation.

## 9. Verification Requirements

Before handoff to Runtime, the following must be explicit:

- target and scope;
- reason for the diagnostic capability;
- diagnostic result classes;
- Evidence boundary;
- API boundary status;
- unresolved semantics.

Before implementation is treated as complete:

- implementation tests exist;
- the actual verification result is recorded;
- the diff is reviewed;
- submission state is checked;
- canonical repository state is confirmed.

## 10. Relationship to One Change, One Verification

Self-Diagnostic does not replace the Shirakami rule:

> One change, one verification.

It provides a later mechanism for inspecting whether the expected state is actually present.

The Submission Check adds a final delivery-state check:

> Test correctness and delivery correctness are separate verification targets.

## 11. Non-Goals

This protocol does not define:

- a self-scoring system;
- an autonomous authority layer;
- a claim that diagnostic output is inherently true;
- provider-specific AI invocation;
- `/diagnostic` or another new public endpoint;
- automatic modification of Runtime or Research semantics.

## 12. Handoff

Current intended flow:

```text
Research
  ↓
Self-Diagnostic meaning / scope
  ↓
的目YAML handoff
  ↓
Runtime implementation
  ↓
Tests / Verification
  ↓
GitHub
  ↓
Operation
  ↓
Evidence
  ↓
Finding / Research feedback
```

The implementation may expose findings that require Research reconsideration. Such findings must return through the handoff mechanism rather than being silently incorporated as theory.

## 13. Canonical Principle

> 自分は正しいと宣言することではなく、現在、自分について何が確認できているかを提示する。

That principle is the boundary of Self-Diagnostic in v0.1.

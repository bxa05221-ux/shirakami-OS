# Reviewer → AIwitness → Traceability Architecture Map

## Purpose

This map defines the observable boundary between independent reviewer input, comparative aggregation, AIwitness provenance, and machine-checkable traceability.

The map is descriptive. It does not grant authority or define a decision.

## Four-layer boundary

```text
Reviewer
  │
  │ reviewer_id / Matome YAML / observation / Evidence IDs / proposal
  ▼
Comparative Trace
  │
  │ reviewer identity / observations / proposals
  │ shared Evidence / divergent Evidence
  │ decision = null
  ▼
AIwitness
  │
  │ provenance / trace role
  │ authority_granted = false
  │ decision_authorized = false
  │ decision = null
  │ human_gate_required = true
  ▼
Traceability
  │
  │ identity / Evidence / verification / commit continuity
  │ authority non-propagation
  ▼
Human Gate
  │
  ▼
Human judgment
```

## Boundary responsibilities

### 1. Reviewer

The reviewer is an observation producer.

The reviewer may provide:

- reviewer identity;
- Matome YAML context;
- observations;
- Evidence IDs;
- proposals.

A proposal remains a proposal. It is not a decision.

### 2. Comparative Trace

The comparative layer makes independent observations comparable without collapsing them into a single judgment.

It preserves:

- reviewer identity;
- Matome YAML;
- observations;
- proposals;
- Evidence IDs;
- shared Evidence;
- divergent Evidence.

Shared and divergent Evidence are kept as separate sets. Their overlap is rejected by comparative traceability validation.

### 3. AIwitness

AIwitness is a provenance and observation boundary.

It carries forward the comparative context while explicitly preserving:

- `decision = null`;
- `authority_granted = false`;
- `decision_authorized = false`;
- `human_gate_required = true`.

AIwitness does not convert agreement, Evidence, verification, or interpretation into authority.

### 4. Traceability

Traceability validates continuity rather than deciding meaning.

The comparative validator rejects:

- a non-null decision;
- granted authority;
- decision authorization;
- removal of the Human Gate;
- overlapping shared/divergent Evidence.

The execution traceability validator additionally checks:

- Evidence identity continuity;
- handoff identity continuity;
- execution identity continuity;
- trace identity continuity;
- witness identity continuity;
- verification-status continuity;
- commit continuity;
- execution/publish/merge authority non-propagation.

## Information preservation rule

The boundary is intentionally asymmetric:

```text
Reviewer
  → more observations

Comparative Trace
  → more comparison structure

AIwitness
  → more provenance

Traceability
  → more validation

None of these steps
  → more authority
```

In particular:

```text
proposal ≠ decision
comparison ≠ judgment
verification ≠ authorization
Evidence ≠ authority
AIwitness ≠ decision-maker
```

## Verification path

A reviewer can inspect the boundary using:

1. `reviewer/registry.py`
2. `reviewer/comparative_trace.py`
3. `reviewer/aiwitness_bridge.py`
4. `aiwitness/traceability.py`
5. `reviewer/test_comparative_aiwitness_integration.py`
6. `aiwitness/test_traceability.py`

The tests are intended to make the boundary executable rather than relying only on documentation.

## Current verification status

This architecture map describes the implementation present on the `phase3-api-boundary` branch.

The latest boundary-test commits are:

- `31c30f92f35a5a316500e80c1df9f98d19109b66` — reviewer proposals remain proposals through AIwitness.
- `6a475e40e3ec216a2c193f4bd646d5b8d7f8d15932` — comparative traceability rejects decision/authority escalation and Evidence overlap.

CI status must be verified separately for these commits; a commit existing in GitHub is not itself evidence that its tests passed.

## Human Gate

This architecture does not transfer authority between agents.

The final judgment remains outside the Reviewer, Comparative Trace, AIwitness, and Traceability layers.

The boundary therefore ends at:

```text
Evidence-backed observation
        ↓
Human Gate
        ↓
Human judgment
```

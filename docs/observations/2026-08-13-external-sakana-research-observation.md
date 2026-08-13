# External Research Observation — Sakana AI α0.1

Date: 2026-08-13
Source: Sakana AI
Observation Type: External Research Landscape Observation
Status: Unverified / Pending Shirakami Review

## Scope

The Shirakami OS repository was provided to Sakana AI as an external Research Landscape.

Sakana was instructed to observe the repository rather than modify it, implement changes, or extend Shirakami theory.

This document records the resulting external observations. It does not promote those observations to Foundation truth.

## Observed Architecture

Sakana reconstructed the repository architecture as:

Human Landscape
→ Protocol / Matome YAML
→ Protocol Loader / Protocol IR
→ Runtime
→ Evidence
→ Landscape State
→ Landscape Adapter
→ Backend / GitHub

The observation confirms that the repository contains a working minimal vertical slice across these boundaries, while also identifying several boundaries that remain incomplete or split across implementations.

## External Observations

### 1. API / Runtime Boundary

Sakana observed that `api/runtime_api.py` directly uses `plugins/adapters/github/github_adapter.py` for GitHub operations, while the documented architecture places Runtime and Landscape Adapter boundaries between API-level execution and the backend.

External question:

Is this a temporary implementation shortcut, or does the API layer intentionally expose a separate adapter path?

### 2. Evidence Persistence Boundary

Sakana observed that Evidence records are immutable in memory, while the persistence responsibility is not yet defined.

External question:

Which layer owns Evidence persistence: Runtime, Adapter, Backend, or a dedicated Store?

### 3. GitHub Adapter Duplication

Sakana observed two GitHub-specific structures:

- `runtime/github_landscape_adapter.py` with `runtime/github_client.py`
- `plugins/adapters/github/github_adapter.py`

External question:

Are these intentionally separate boundaries, or should one eventually become the canonical GitHub integration path?

### 4. Runtime Replaceability

Sakana observed that Runtime replaceability is currently an architectural principle rather than a cross-runtime conformance claim.

External question:

What evidence would be sufficient to demonstrate that a second Runtime implementation can consume the same Protocol / IR contract?

### 5. Plugin / Runtime Boundary

Sakana observed that Plugin declarations and RFCs exist while Plugin infrastructure is intentionally not integrated into the Runtime core.

External question:

Is this declaration-first sequencing intentional, or is the Plugin boundary still under architectural reconsideration?

## Important Contradiction Observation

The external observation concerning the API / Runtime boundary should be compared against the existing β0.1 Final Gate observation.

The Final Gate records the intended Runtime → Adapter → GitHub boundary as verified for the current implementation phase.

Therefore this external observation must not be interpreted as proof that the Final Gate is incorrect. It identifies a potentially observable difference between the declared boundary and one API implementation path.

This discrepancy itself is the Evidence candidate for the next review cycle.

## Newly Observable Research Questions

The following questions are promoted for review, not for immediate implementation:

1. API → Runtime → Adapter boundary consistency
2. Evidence persistence responsibility
3. Canonical GitHub Adapter boundary

Secondary questions:

4. Runtime conformance / replaceability evidence
5. Plugin → Runtime integration timing

## Action Policy

No Foundation theory is changed by this observation.

No Runtime implementation is changed by this observation.

No Plugin architecture is changed by this observation.

The next step is to compare these external observations with the existing repository evidence and determine which questions require implementation work.

## Observation Principle

External observation is not truth.

The value of this observation is the newly visible relation between the existing Shirakami Landscape and an independent Research Landscape.

The human remains authoritative over Foundation decisions.

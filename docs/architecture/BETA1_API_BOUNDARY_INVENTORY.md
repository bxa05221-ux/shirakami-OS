# Shirakami β1.0 API Boundary Inventory

Status: research / architecture inventory
Scope: existing API-related artifacts on `main`

## Purpose

This document inventories the existing API surfaces before selecting a formal β1.0 external API boundary.
It does not introduce new Runtime theory or change API behavior.

## Inventory

### 1. `shbb-api/`

**Role:** external Shirakami API boundary candidate.

Current surface:

- `POST /observe`
- FastAPI application in `shbb-api/app.py`
- OpenAPI contract in `shbb-api/openapi.yaml`
- HTTP contract tests in `tests/test_shbb_api.py`

Boundary intent:

```text
Client
  ↓
Shirakami API
  ↓
Runtime
  ↓
Landscape / Evidence / Protocol / State Transition
  ↓
Adapter
  ↓
External AI / Backend
```

Current status in its own documentation: `experimental / implementation candidate`.

### 2. `api/`

**Role:** existing API module family.

Observed artifacts include Runtime-facing API modules such as `api/__init__.py` and related API implementations.

This family should not automatically be treated as the public β1.0 boundary without further classification.

### 3. `runtime/protocol_api.py`

**Role:** Protocol invocation boundary inside the Runtime architecture.

This is relevant to Runtime integration, but its existence does not by itself establish the public external API contract.

### 4. `runtime/wayfinding_api.py`

**Role:** application/domain-specific API surface.

It should remain distinct from the generic Shirakami external API boundary unless a later specification explicitly promotes it.

## Preliminary classification

| Surface | Primary role | β1.0 public boundary candidate |
|---|---|---|
| `shbb-api/` | External Shirakami API | **Yes** |
| `api/` | Existing API module family | Not yet |
| `runtime/protocol_api.py` | Runtime / Protocol invocation | Not as public boundary by default |
| `runtime/wayfinding_api.py` | Application-specific API | No |

## Proposed boundary principle

For β1.0, `shbb-api/` is the single external API boundary candidate.

The first contract remains intentionally minimal:

```text
POST /observe
```

The API must expose the existing Runtime boundary rather than become a new domain-logic layer.

## Contract constraints

- Landscape remains the continuity boundary.
- Protocol remains the semantic authority.
- Runtime executes and observes.
- Evidence is not fabricated by the API layer.
- Adapter remains replaceable.
- AI self-report is not verification evidence by itself.
- Unverified behavior is not reported as successful.
- No new theory is introduced at the API layer.

## Current implementation observation

The current `/observe` implementation constructs a `LandscapeState` from the supplied input and returns an observation result with provenance. The current implementation explicitly reports `transition: false` and leaves `evidence_id` null rather than inventing an Evidence record.

This is consistent with a minimal observation boundary, but does not yet establish production readiness.

## Verification required before formal API freeze

1. Confirm the external process boundary with an actual HTTP client/server run.
2. Confirm OpenAPI and implementation behavior remain aligned.
3. Confirm existing API modules do not duplicate or contradict the selected public boundary.
4. Confirm error behavior and unresolved Evidence semantics.
5. Confirm documentation and Quickstart point to the same public boundary.
6. Run the repository's required Runtime/API tests and CI.

## Non-goals

This inventory does not:

- redesign the Runtime,
- add `/chat` or `/generate`,
- define provider-specific AI APIs,
- claim production readiness,
- redefine Evidence semantics,
- rename the repository.

## Decision point

After verification, the repository may freeze `shbb-api/` as the β1.0 external API boundary and document its supported contract separately from historical or application-specific APIs.

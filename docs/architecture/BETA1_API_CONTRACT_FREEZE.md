# Shirakami β1.0 External API Contract Freeze

Status: **β1.0 boundary candidate — contract frozen for the current prototype baseline**

This document records the smallest external HTTP contract currently verified for Shirakami. It does not redesign the Runtime or define a production API.

## 1. Boundary

The current external API boundary is `shbb-api`.

The single public operation covered by this freeze is:

```text
POST /observe
```

The boundary exposes observation only. It does not expose a generic chat, generation, agent, or provider-specific interface.

## 2. Request contract

Required fields:

- `landscape_id`: non-empty string identifying the target Landscape.
- `input`: JSON object containing observable input.

Optional fields:

- `protocol_id`: explicitly selected Protocol reference.
- `metadata`: client metadata. Metadata is not treated as domain truth.

The implementation rejects a missing/empty `landscape_id` and a non-object `input` with HTTP 400.

## 3. Response contract

A successful observation returns:

- `landscape_id`
- `observation_id`
- `state` = `observed`
- `evidence_id` (currently nullable and normally `null` at this boundary)
- `protocol_id` (nullable when not supplied)
- `result`
- `provenance`

The current implementation explicitly reports `provenance.transition = false`. The `/observe` boundary therefore does not claim that an observation itself constitutes a state transition.

## 4. Error boundary

The currently verified client-visible error is:

```text
HTTP 400 — invalid request
```

The OpenAPI contract also reserves 404, 409, and 500 response classes for future Runtime behavior. Their detailed semantics are **not frozen by this document** and must not be inferred from their presence in OpenAPI alone.

## 5. OpenAPI ↔ implementation ↔ test

The contract is represented by:

- `shbb-api/openapi.yaml`
- `shbb-api/app.py`
- `tests/test_shbb_api.py`
- `tests/test_shbb_api_process.py`

Verification has two levels:

1. in-process HTTP testing with FastAPI `TestClient`;
2. actual HTTP process-boundary testing through a separately launched `uvicorn` process.

The process-boundary test exercises `/observe` over HTTP and verifies both the successful observation response and invalid-input rejection.

## 6. Evidence semantics

This freeze does **not** redefine Evidence.

`evidence_id` remains nullable because the current `/observe` implementation is an observation boundary rather than a claim that every request has already produced finalized Evidence.

The API must not manufacture Evidence merely to make a response appear complete.

## 7. Protocol and Runtime boundary

`protocol_id` is a reference supplied by the client when explicitly selected. The API does not reinterpret Protocol semantics.

The Runtime remains responsible for execution and observable Runtime state. The API is an external transport boundary over that existing responsibility.

## 8. What is frozen

For the current PV1.0 / β1.0 Operational Rollout baseline, the following are frozen as the minimal external boundary:

```text
external client
    ↓
POST /observe
    ↓
Shirakami Runtime boundary
    ↓
Landscape observation
    ↓
observable response
```

Frozen means that future changes must be treated as deliberate contract changes, with their own verification and review.

## 9. What is not frozen

The following remain outside this contract freeze:

- authentication and authorization
- production deployment
- rate limiting
- persistent Evidence storage
- full Protocol execution through HTTP
- state-conflict semantics beyond the reserved OpenAPI response class
- external repository synchronization
- provider-specific AI invocation
- `/chat`, `/generate`, or agent endpoints
- robot or physical-device control endpoints

These may become later research or implementation targets, but their absence is intentional in the current boundary.

## 10. Verification rule

Any change to this boundary follows the Shirakami change-control rule:

> One change, one verification.

Contract changes require:

- explicit target and scope;
- implementation/OpenAPI alignment;
- corresponding tests;
- local/CI verification;
- review before merge;
- explicit recording of unresolved semantics.

## 11. Relationship to PV1.0

PV1.0 establishes the first operational prototype baseline. This contract freeze establishes the smallest externally observable API boundary for that baseline.

It does **not** mean that the Shirakami API is feature-complete or production-ready.

The intended progression remains:

```text
PV1.0
  ↓
Protocol First
  ↓
External API Boundary
  ↓
Operation
  ↓
Evidence
  ↓
Finding / Revision
```

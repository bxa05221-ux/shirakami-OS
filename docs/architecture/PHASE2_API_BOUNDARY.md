# Shirakami Phase 2 — External API Boundary

Status: **Phase 2 boundary freeze candidate**

## Purpose

Phase 2 begins by extracting the already-verified Shirakami semantic boundary without expanding authority.

The existing `shbb-api` surface is deliberately small:

```text
External Client
    ↓
POST /observe
    ↓
Landscape observation
    ↓
Observable response
```

This is an API boundary, not an agent endpoint and not a generic execution gateway.

## Frozen responsibility

The external API may:

- accept an explicit Landscape observation;
- preserve an explicitly supplied `protocol_id` as a reference;
- return an observable result;
- return provenance;
- return an observation identity;
- reject malformed or invalid input.

The external API must not:

- approve a Protocol;
- promote a Protocol Candidate;
- create an Approval Envelope;
- grant execution authorization;
- broaden execution scope;
- reinterpret verification mismatch as success;
- silently mutate an Approved Protocol;
- select a candidate on behalf of a Human;
- expose provider-specific AI invocation as the semantic contract.

## Authority rule

The API is a transport/interface boundary.

It consumes or reports information; it does not manufacture authority.

```text
Human decision
    ↓
Approval Envelope / Human Gate
    ↓
Activation
    ↓
Execution control
    ↓
Runtime
    ↓
Verification
    ↓
Evidence
```

The observation API sits beside this lifecycle rather than replacing its authorization boundary.

## Current endpoint

`POST /observe`

The current contract is frozen as the minimum external boundary for the PV1.0 / β1.0 prototype baseline.

No `/chat`, `/generate`, generic agent, or provider-specific endpoint is introduced by this Phase 2 step.

## Verification

The API boundary is verified through:

1. OpenAPI contract;
2. in-process FastAPI tests;
3. process-boundary HTTP tests;
4. explicit invalid-input tests;
5. authority-boundary tests.

Change-control remains:

> One change, one verification.

## Phase 2 implication

API extraction does not mean API expansion.

The goal is to make the Shirakami semantic boundary reusable by multiple UIs, runtimes, devices, and future adapters while keeping authority outside the transport layer.

The next API work should therefore focus on **stable semantic handoff**, not feature proliferation.

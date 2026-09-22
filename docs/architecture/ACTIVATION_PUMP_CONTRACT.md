# Activation Pump Contract

## Purpose

The Activation Pump is a downstream execution-control mechanism. It consumes an
already-authorized Activation Request and hands it to the Runtime at an
explicitly requested time or trigger.

The Activation Pump is **not** an approval mechanism.

## Boundary

```
Approved Protocol
      |
      v
Approval Envelope
      |
      v
Activation Request
      |
      v
Activation Pump
      |
      v
Runtime Execution
      |
      v
Verification
      |
      v
Evidence
```

The Pump may transport, queue, delay, retry, or release an already-authorized
activation request according to explicit execution policy.

## Non-responsibilities

The Activation Pump MUST NOT:

1. create or modify an Approval Envelope;
2. promote a Protocol Candidate;
3. perform Human Gate approval;
4. select a Protocol Candidate;
5. infer execution authority from context;
6. broaden the approval scope;
7. convert failed verification into success;
8. silently change the Protocol or its provenance;
9. treat scheduling as authorization;
10. grant publication authority.

## Minimum input contract

An Activation Pump input MUST contain:

- an already-validated Activation Request or equivalent immutable handoff;
- the Protocol identity;
- explicit execution authorization;
- the associated Approval Envelope;
- execution context;
- an observable trigger or release condition.

If the authorization is missing, inconsistent, or invalid, the Pump MUST fail
closed and MUST NOT invoke Runtime execution.

## Release semantics

A Pump release is an execution-control event, not a governance event.

The following distinction is normative:

- **Approval** answers: "May this Protocol execute?"
- **Activation** answers: "Prepare this authorized Protocol for execution."
- **Pump release** answers: "Release this already-authorized activation now."
- **Runtime** answers: "Execute the Protocol and report the transition."
- **Verification** answers: "Does the observed transition match the declared expectation?"
- **Evidence** answers: "What was observed and recorded?"

No downstream stage may retroactively answer an upstream governance question.

## Retry semantics

Retries MAY repeat an already-authorized activation only within the original
authorization scope.

A retry MUST NOT:

- create a new approval;
- alter candidate or Protocol identity;
- broaden execution scope;
- suppress previous Evidence;
- reinterpret a mismatch as success.

Each retry SHOULD remain observable as a distinct execution-control event.
Event identity must not be confused with content identity of Evidence artifacts.

## Scheduling

Scheduling is deliberately outside this contract.

A future scheduler may provide:

- time-based release;
- event-based release;
- queue management;
- backoff and retry policy.

It MUST consume this contract rather than redefine it.

## Relationship to Background Runner

The Background Runner is a separate downstream concern.

The Pump controls **release**.

The Runner controls **ongoing execution context**.

Neither component grants authority.

## Failure behavior

Invalid or expired authorization, mismatched Protocol identity, malformed
activation data, or violated execution scope MUST produce an observable failure
and MUST NOT invoke Runtime.

This preserves the fail-closed property of the Shirakami execution path.

## Design principle

> Generation may be automated. Promotion remains human-authorized.
> Activation prepares. Pump release schedules. Execution remains observable.

## Scope

This document defines the governance boundary only. It does not define a
scheduler, queue implementation, worker pool, concurrency model, persistence
backend, or background service.

# Approved Protocol → Activation Boundary

## Purpose

This document defines the boundary between an **Approved Protocol** and its runtime activation.

The boundary exists because approval and activation answer different questions:

- **Human Gate / Approval Envelope:** Is this candidate authorized for execution?
- **Activation:** Is an already-authorized Protocol prepared and admitted to the Runtime execution environment?

Activation must never become an implicit approval mechanism.

## Lifecycle

```text
Protocol Candidate
      |
      v
Structural Validation
      |
      v
HUMAN_REVIEW
      |
      v
Human Gate
      |
      v
Approval Envelope
      |
      v
Approved Protocol
      |
      v
Activation
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

## Boundary Rules

### 1. Activation consumes authorization; it does not create authorization

An Activation component MUST require an explicit, valid authorization state before preparing a Protocol for execution.

It MUST NOT:

- select a candidate,
- infer human approval,
- manufacture an Approval Envelope,
- promote a Candidate to Approved,
- treat successful preparation as approval.

### 2. Approved Protocol is the input boundary

Activation operates only on an Approved Protocol together with the authorization metadata required by the Runtime.

The minimum conceptual handoff is:

```text
Approved Protocol
+ Approval Envelope
+ Runtime context
→ Activation request
```

The Approval Envelope remains the authoritative record that execution was explicitly authorized.

### 3. Preparation is not execution

Activation may validate preconditions, resolve resources, load a Protocol, or prepare an execution environment.

A successful activation MUST NOT be interpreted as evidence that the Protocol has executed successfully.

Execution and verification remain downstream Runtime responsibilities.

### 4. Activation failure is observable

Activation failures MUST remain observable and attributable to the activation attempt.

Where practical, the resulting Evidence should preserve:

- Protocol identity,
- Approval Envelope identity or authorization context,
- activation status,
- failure or success reason,
- relevant Runtime context.

Activation failure MUST NOT silently alter the Approved Protocol.

### 5. Activation does not mutate the Protocol

Activation may provision or prepare Runtime resources, but it MUST NOT rewrite the approved Protocol artifact.

If preparation requires a changed Protocol, that changed artifact is a new candidate and must re-enter the promotion lifecycle.

## Relationship to RFC-0003

RFC-0003 defines Plugin Activation as a Runtime lifecycle responsibility: discovered capabilities are transitioned to a prepared state before execution.

This document narrows that concept for the current Shirakami lifecycle:

- discovery may produce candidates,
- Human Gate establishes authorization,
- Approved Protocol crosses the activation boundary,
- Activation prepares an authorized Protocol,
- Runtime executes it.

Thus, **activation is a downstream lifecycle transition, not a governance transition**.

## Activation Pump

The previously discussed "Activation Pump" is therefore treated as an implementation mechanism for this boundary, not as an approval mechanism.

An Activation Pump may:

1. receive an already-approved activation request,
2. validate the Approval Envelope,
3. prepare the Protocol and required Runtime resources,
4. emit an observable activation result,
5. hand the prepared execution to the Runtime.

It MUST NOT:

- auto-approve candidates,
- bypass Human Gate,
- convert Evidence directly into execution authority,
- silently promote Protocol Candidates.

## Background Runner

A Background Runner is a separate downstream concern.

It may consume activation requests that are already authorized, but scheduling, repetition, or background execution MUST NOT create authority that does not already exist.

Therefore:

```text
Human Gate
  ↓
Approval Envelope
  ↓
Approved Protocol
  ↓
Activation Pump
  ↓
Background Runner (optional)
  ↓
Runtime
```

The Background Runner remains out of scope for this boundary document.

## Design Principle

> **Generation may be automated. Promotion remains human-authorized. Activation prepares. Execution remains observable.**

This boundary deliberately keeps governance and execution mechanics separate.

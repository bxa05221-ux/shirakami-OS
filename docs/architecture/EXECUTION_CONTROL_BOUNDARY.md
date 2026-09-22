# Execution Control Boundary

## Purpose

This document closes the first-stage Shirakami execution-control boundary.

The system permits automated generation and repeated execution while keeping authorization outside the execution mechanisms.

## Closed lifecycle

Protocol Candidate → Structural Validation → HUMAN_REVIEW → Approval Envelope → Human Gate → Approved Protocol → Activation → Activation Pump release → Background Runner → Runtime → Verification → Evidence → Landscape.

## Authority rule

Only the upstream approval path creates execution authority.

- Candidate generation does not authorize execution.
- Structural validation does not authorize execution.
- Activation consumes authorization.
- Activation Pump releases an already-authorized activation.
- Background Runner maintains bounded execution context.
- Runtime executes; it does not promote authority.
- Verification records pass or mismatch.
- Evidence records what happened; it does not silently authorize a new protocol.

The internal activated_execution transition only synchronizes Runtime lifecycle state with an externally authorized Activation. It is not itself an approval mechanism.

## Fail-closed conditions

Execution stops when Activation or Pump release is invalid, Protocol identity is missing or inconsistent, Runtime lifecycle cannot enter the authorized execution state, Runner iteration budget is invalid, or Verification reports a mismatch.

A verification mismatch does not become success and does not broaden authority.

## Background Runner boundary

The Runner may maintain a bounded run identifier, repeat an already-authorized execution cycle, preserve Protocol identity, stop on mismatch, and expose each iteration as an observable execution-control result.

It must not approve or reject Protocols, promote or select candidates, create Approval Envelopes, broaden execution scope, schedule future work, create worker pools or persistence services, or reinterpret verification failure as success.

## Design principle

> Generation may be automated. Promotion remains human-authorized. Activation prepares. Pump releases. Runner continues bounded execution. Execution remains observable.

This closes the first-stage control-plane boundary without claiming that scheduling, persistence, provider integration, or automatic Protocol generation are complete.
